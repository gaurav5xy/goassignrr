import requests
import openai
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import pytesseract
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO
from reportlab.lib.units import inch
from django.views.generic import TemplateView

openai.api_key = settings.OPENAI_API_KEY
content_text = ''

class GoogleSearchConsoleView(TemplateView):
    template_name = 'google5c48ed90c9c2a47a.html'

def submit_topic(request):
    return render(request, 'index.html')

def generate_content_internal(request, content_type, template):
    global content_text
    if request.method == 'GET':
        topic = request.GET.get('topic', '')
        # word_count = int(request.GET.get('word_count', 500))
        word_count_str = request.GET.get('word_count', '500')
        try:
            word_count = int(word_count_str)
        except ValueError:
            word_count = 500
        
        if topic:
            # Change the prompt here for assignment and essay
            if content_type == "Assignment":
                prompt = f"Please write a {word_count}-word assignment on the topic of ```{topic}```."
            elif content_type == "Essay":
                prompt = f"Please write a {word_count}-word essay on the topic of ```{topic}```."
            else:
                prompt = f"Please write a {word_count}-word text on the topic of ```{topic}```."
            
            try:
                response = requests.post(
                    "https://api.openai.com/v1/engines/text-davinci-003/completions",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {openai.api_key}",
                    },
                    json={
                        "prompt": prompt,
                        "max_tokens": word_count,  # Increased max_tokens for longer content
                    }
                )

                # print("OpenAI API Response:")
                # print(response.json())

                # Check for successful response status
                if response.status_code == 200:
                    response_data = response.json()
                    choices = response_data.get('choices')
                    if choices and len(choices) > 0:
                        content_text = choices[0].get('text')
                    else:
                        content_text = f"No text available"
                    # print(f"Generated {content_type}: {content_text}")    
                else:
                    content_text = f"Error: Sorry, we couldn't generate content for this topic at the moment. Please try again later or choose a different topic."
            except requests.exceptions.RequestException as e:
                content_text = f"Error: Oops, it seems we're experiencing a temporary connection issue. Please check your internet connection and try again."
        
            is_ajax_request = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

            if is_ajax_request:
                return JsonResponse({f'{content_type.lower()}_text': content_text})
            else:
                context = {f'{content_type.lower()}_text': content_text}
                return render(request, template, context)

    return render(request, 'index.html')

def generate_assignment(request):
    return generate_content_internal(request, "Assignment", 'assignments/generate_assignment.html')

def generate_essay(request):
    return generate_content_internal(request, "Essay", 'essay/generate_essay.html')

def download_pdf(request):
    global content_text

    if not content_text:
        return render(request, 'no_content.html')
    
    try:
        # Create a BytesIO buffer for the PDF
        pdf_buffer = BytesIO()
        
        # Create a PDF document
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        story = []
        
        # Create a custom style with increased font size and line spacing
        custom_style = ParagraphStyle(name='CustomStyle', parent=getSampleStyleSheet()["Normal"])
        custom_style.fontSize = 14  # Adjust the font size here
        custom_style.leading = 18  # Adjust the line spacing (leading) here
        
        # Split the content_text into paragraphs and add new lines
        paragraphs = content_text.split('\n')
        
        # Add each paragraph to the PDF using the custom style
        for paragraph_text in paragraphs:
            paragraph = Paragraph(paragraph_text, style=custom_style)
            story.append(paragraph)
            story.append(Paragraph("<br /><br />", style=custom_style))  # Add new line
            
        # Build the PDF document
        doc.build(story)
        
        # Retrieve PDF data from the buffer
        pdf_data = pdf_buffer.getvalue()
        
        # Set response headers for PDF download
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=generated_assignment.pdf"
        
        # Write PDF data to the response
        response.write(pdf_data)
        content_text = ''
        return response
    except Exception as e:
        error_message = f"We apologize, but there was an issue generating the PDF. Our team has been notified, and we're working to fix it. Please try downloading your content later."
        return HttpResponse(error_message, status=500)
