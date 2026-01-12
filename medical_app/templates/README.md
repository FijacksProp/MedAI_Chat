# MedAI Assistant - Frontend Documentation

A modern, professional, and interactive medical AI assistant interface built with HTML, Tailwind CSS, and JavaScript. Ready for Django integration.

## 🎨 Design Features

- **Clean, Professional Aesthetic**: White background with calming blue-green gradients
- **Medical-Themed Animations**: Floating health icons, pulse waves, and DNA strands
- **Fully Responsive**: Optimized for desktop, tablet, and mobile devices
- **Smooth Interactions**: Hover effects, transitions, and micro-animations
- **Accessibility**: Semantic HTML, keyboard navigation, and focus indicators

## 📁 File Structure

```
medical-ai-assistant/
│
├── base.html           # Base template with shared styling and animations
├── landing.html        # Landing page with intake form
├── chat.html          # Chat interface for AI conversation
└── README.md          # This file
```

## 🚀 Django Integration Guide

### 1. Setup Static Files

In your Django `settings.py`:

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

### 2. Configure Templates

Place the HTML files in your Django templates directory:

```
your_project/
├── templates/
│   ├── base.html
│   ├── landing.html
│   └── chat.html
```

### 3. Update URLs

In your `urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('chat/', views.chat_view, name='chat'),
]
```

### 4. Create Views

In your `views.py`:

```python
from django.shortcuts import render

def landing_view(request):
    return render(request, 'landing.html')

def chat_view(request):
    return render(request, 'chat.html')
```

### 5. API Integration

To connect with your AI backend, modify the `generateFollowUpResponse` function in `chat.html`:

```javascript
// Replace the placeholder function with an actual API call
async function generateFollowUpResponse(userMessage) {
    try {
        const response = await fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),  // Django CSRF token
            },
            body: JSON.stringify({
                message: userMessage,
                history: conversationHistory,
                intake_data: intakeData
            })
        });
        
        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('Error:', error);
        return '<p>I apologize, but I encountered an error. Please try again.</p>';
    }
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```

## 🎯 Key Features

### Landing Page (landing.html)

- **Intake Form** with validation
- **Fields collected**:
  - Age range (required)
  - Sex (optional)
  - Main symptom (required, free text)
  - Duration (required, dropdown)
  - Severity (required, 1-5 scale with emojis)
  - Additional context (optional, textarea)
- **Smooth page transition** to chat interface
- **Form data stored** in sessionStorage for chat page access

### Chat Interface (chat.html)

- **Patient summary card** displaying intake information
- **Message bubbles** distinguishing user and AI
- **Typing indicator** during AI response
- **Collapsible sections** for structured AI responses:
  - Possible Causes
  - Self-Care Advice
  - When to Seek Immediate Care
  - When to See a Doctor
- **Severity badges** with color coding
- **Auto-scrolling** to latest messages
- **Input field** with auto-resize
- **Send on Enter** (Shift+Enter for new line)

## 🎨 Customization

### Colors

Edit CSS variables in `base.html`:

```css
:root {
    --color-primary: #0EA5E9;      /* Main blue */
    --color-secondary: #06B6D4;    /* Cyan */
    --color-accent: #10B981;       /* Green */
    --color-light: #F0F9FF;        /* Light blue */
    --color-white: #FFFFFF;        /* White */
    /* ... add more custom colors ... */
}
```

### Typography

Change fonts by updating the Google Fonts import in `base.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=YourFont:wght@400;500;700&display=swap" rel="stylesheet">
```

Then update the CSS:

```css
body {
    font-family: 'YourFont', sans-serif;
}
```

### Animations

Adjust animation speeds in the `@keyframes` rules or disable specific animations by commenting out the relevant divs in the animated background section.

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## ♿ Accessibility Features

- Semantic HTML5 elements
- Proper ARIA labels
- Keyboard navigation support
- Focus indicators
- Screen reader friendly
- Color contrast compliant

## 🔒 Security Considerations

1. **Never store sensitive health data in sessionStorage in production**
   - Use secure server-side sessions instead
   - Encrypt sensitive data
   - Implement proper authentication

2. **CSRF Protection**
   - Ensure Django CSRF tokens are included in AJAX requests
   - Use `{% csrf_token %}` in forms

3. **Input Validation**
   - Client-side validation is implemented
   - Always validate server-side as well
   - Sanitize user inputs

## 🧪 Testing Checklist

- [ ] Form validation works correctly
- [ ] Page transition is smooth
- [ ] Data persists from landing to chat
- [ ] Chat messages display properly
- [ ] Collapsible sections toggle correctly
- [ ] Typing indicator appears and disappears
- [ ] Responsive design works on all devices
- [ ] Animations don't cause performance issues
- [ ] Keyboard navigation works
- [ ] CSRF tokens are properly handled

## 🐛 Troubleshooting

### Page doesn't transition to chat
- Check browser console for JavaScript errors
- Verify sessionStorage is available
- Ensure URL in form submission matches Django route

### Animations lag or stutter
- Reduce number of animated particles
- Simplify animation keyframes
- Use `will-change` CSS property sparingly

### Styles not loading
- Verify Tailwind CDN is accessible
- Check for CSS conflicts with existing styles
- Ensure template inheritance is correct

## 📦 Production Checklist

- [ ] Replace Tailwind CDN with compiled CSS
- [ ] Minify JavaScript
- [ ] Optimize images and SVGs
- [ ] Enable browser caching
- [ ] Implement proper error handling
- [ ] Add loading states for API calls
- [ ] Set up error logging
- [ ] Add rate limiting for API endpoints
- [ ] Implement proper authentication
- [ ] Add medical disclaimer

## 📄 Medical Disclaimer Template

Add this to your landing page footer:

```html
<div class="disclaimer text-sm text-gray-600 mt-8 p-4 bg-gray-50 rounded-lg">
    <strong>⚠️ Medical Disclaimer:</strong> This AI assistant provides general health information only 
    and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the 
    advice of your physician or other qualified health provider with any questions you may have regarding 
    a medical condition. Never disregard professional medical advice or delay in seeking it because of 
    something you have read here. If you think you may have a medical emergency, call your doctor or 
    emergency services immediately.
</div>
```

## 🤝 Contributing

To extend this interface:

1. Maintain the design system (colors, typography, spacing)
2. Follow accessibility guidelines
3. Test on multiple devices and browsers
4. Document any new features
5. Keep animations subtle and purposeful

## 📧 Support

For questions or issues:
- Check the troubleshooting section
- Review Django and Tailwind documentation
- Test in different browsers

## 🎉 Credits

- **Fonts**: DM Sans & Fraunces from Google Fonts
- **CSS Framework**: Tailwind CSS
- **Icons**: Custom SVG medical icons
- **Design**: Medical-tech aesthetic with calm, professional styling

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**License**: MIT (adjust as needed)
