from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
import json
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

# Create your views here.

@ensure_csrf_cookie
def landing_view(request):
    """Landing page with intake form"""
    return render(request, 'landing.html')

@ensure_csrf_cookie
def chat_view(request):
    """Chat interface page"""
    return render(request, 'chat.html')

def chat_api(request):
    """API endpoint for chat messages"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            conversation_history = data.get('history', [])
            intake_data = data.get('intake_data', {})

            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Create the model (using Gemini 1.5 Flash - better free tier limits)
            model = genai.GenerativeModel('gemini-2.5-flash')

            # Build the system prompt with medical guidelines
            system_context = """You are MedAI, a compassionate and knowledgeable medical AI assistant. Your role is to provide evidence-based health information and guidance while maintaining appropriate medical boundaries.

IMPORTANT GUIDELINES:
1. Be empathetic, supportive, and use clear language
2. Provide general health information and education
3. Always emphasize that you're not a substitute for professional medical advice
4. Never provide specific medical diagnoses or prescriptions
5. Focus on self-care guidance and when to seek medical attention
6. If symptoms sound serious or life-threatening, strongly urge immediate medical attention
7. Structure responses clearly with sections like "Possible Causes", "Self-Care Advice", "When to See a Doctor"
8. Use HTML formatting for better readability (paragraphs, lists, bold text)

EMERGENCY SYMPTOMS that require immediate medical attention:
- Difficulty breathing or shortness of breath
- Chest pain or pressure
- Severe bleeding
- Loss of consciousness or severe confusion
- Severe allergic reactions
- Suspected stroke symptoms (FAST: Face drooping, Arm weakness, Speech difficulty, Time to call 911)
- Severe abdominal pain
- High fever (above 103°F/39.4°C) with other serious symptoms
"""

            # Add patient intake data to context
            if intake_data:
                system_context += f"""

PATIENT INFORMATION:
- Age Range: {intake_data.get('ageRange', 'Not specified')}
- Sex: {intake_data.get('sex', 'Not specified')}
- Main Symptom: {intake_data.get('symptom', 'Not specified')}
- Duration: {intake_data.get('duration', 'Not specified')}
- Severity (1-5): {intake_data.get('severity', 'Not specified')}
- Additional Context: {intake_data.get('context', 'None provided')}
"""

            # Build conversation history for context
            if conversation_history:
                system_context += "\n\nRECENT CONVERSATION:\n"
                # Keep last 6 messages (3 exchanges) for context
                recent_history = conversation_history[-6:]
                for msg in recent_history:
                    role = msg.get('role', '')
                    content = msg.get('content', '')
                    
                    if role == 'user':
                        system_context += f"Patient: {content}\n"
                    elif role == 'assistant':
                        # Strip HTML tags for context
                        import re
                        clean_content = re.sub(r'<[^>]+>', '', content)
                        # Limit length to avoid token issues
                        clean_content = clean_content[:500] + '...' if len(clean_content) > 500 else clean_content
                        system_context += f"You: {clean_content}\n"

            # Create the full prompt
            full_prompt = f"""{system_context}

CURRENT PATIENT MESSAGE:
{user_message}

Please provide a helpful, medically-informed response. Use HTML formatting (paragraphs, bold text, lists) to make your response clear and easy to read. Structure your response with appropriate sections if needed."""

            # Generate response from Gemini
            response = model.generate_content(full_prompt)

            # Check if response was successful
            if response and response.text:
                return JsonResponse({
                    'response': response.text,
                    'status': 'success'
                })
            else:
                return JsonResponse({
                    'error': 'No response generated from AI',
                    'status': 'error'
                }, status=500)

        except Exception as e:
            print(f"Error in chat_api: {str(e)}")  # Log error for debugging
            return JsonResponse({
                'error': 'An error occurred while processing your request',
                'details': str(e),
                'status': 'error'
            }, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def initial_consultation_api(request):
    """API endpoint for generating the initial consultation response"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            intake_data = data.get('intake_data', {})

            if not intake_data:
                return JsonResponse({'error': 'No intake data provided'}, status=400)

            # Create the model (using Gemini 1.5 Flash - better free tier limits)
            model = genai.GenerativeModel('gemini-2.5-flash')

            # Build the prompt for initial consultation
            prompt = f"""You are MedAI, a compassionate medical AI assistant. A patient has just shared their symptoms with you. Provide a thorough initial assessment.

PATIENT INFORMATION:
- Age Range: {intake_data.get('ageRange', 'Not specified')}
- Sex: {intake_data.get('sex', 'Not specified')}
- Main Symptom: {intake_data.get('symptom', 'Not specified')}
- Duration: {intake_data.get('duration', 'Not specified')}
- Severity (1-5): {intake_data.get('severity', 'Not specified')}
- Additional Context: {intake_data.get('context', 'None provided')}

INSTRUCTIONS:
1. Start with a warm, empathetic greeting
2. Provide an initial assessment with possible causes (use collapsible HTML sections)
3. Offer evidence-based self-care advice
4. If severity is 4-5, include urgent care warning
5. Explain when to see a doctor
6. End by asking if they have questions

FORMAT YOUR RESPONSE WITH HTML:
- Use <p> for paragraphs
- Use <strong> for emphasis
- Use <ul> and <li> for lists
- Create collapsible sections like this:

<div class="collapsible-section active">
    <div class="collapsible-header" onclick="toggleCollapsible(this)">
        <span>🔍 Section Title</span>
        <span class="collapsible-icon">▼</span>
    </div>
    <div class="collapsible-content">
        <div class="collapsible-body">
            Content here with <strong>bold text</strong> and lists
        </div>
    </div>
</div>

Create sections for: Possible Causes, Self-Care Advice, When to See a Doctor, and (if severe) When to Seek Immediate Care.

Provide a comprehensive, caring, and medically-informed initial assessment."""

            # Generate response
            response = model.generate_content(prompt)

            if response and response.text:
                return JsonResponse({
                    'response': response.text,
                    'status': 'success'
                })
            else:
                return JsonResponse({
                    'error': 'No response generated',
                    'status': 'error'
                }, status=500)

        except Exception as e:
            print(f"Error in initial_consultation_api: {str(e)}")
            return JsonResponse({
                'error': 'An error occurred',
                'details': str(e),
                'status': 'error'
            }, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)