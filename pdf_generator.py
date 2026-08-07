import re
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter


def format_markdown_for_pdf(text):
    if not text or text.strip() == "" or text == "Not Available":
        return "<i>Not Available</i>"

    # Replace markdown bold **text** with <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Replace markdown italic *text* with <i>text</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Replace markdown headings # Heading with <b>Heading</b>
    text = re.sub(r'^#+\s*(.*?)$', r'<b>\1</b>', text, flags=re.MULTILINE)
    # Replace newlines with <br/>
    text = text.replace('\n', '<br/>')
    return text


def create_section_header(title, bg_color="#1E293B"):
    header_style = ParagraphStyle(
        'SectionHeaderStyle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13,
        textColor=colors.white
    )
    p = Paragraph(f"<b>{title}</b>", header_style)
    t = Table([[p]], colWidths=['100%'])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg_color)),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t


def generate_pdf_report(
    filename,
    resume_analysis,
    career_advice,
    resume_improvement,
    rewritten_resume
):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=10
    )

    title_style = ParagraphStyle(
        'ReportTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.white
    )

    subtitle_style = ParagraphStyle(
        'ReportSubtitle',
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#94A3B8')
    )

    story = []

    # ---------------- Top Banner ---------------- #
    header_content = [
        [Paragraph("AI RESUME ANALYZER REPORT", title_style)],
        [Paragraph("Comprehensive AI-Generated Resume Analysis & Career Report", subtitle_style)]
    ]
    banner = Table(header_content, colWidths=['100%'])
    banner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1E293B')),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
    ]))
    story.append(banner)
    story.append(Spacer(1, 20))

    # ---------------- Section 1: Resume Analysis ---------------- #
    story.append(create_section_header("📄 RESUME ANALYSIS", "#2563EB"))
    story.append(Spacer(1, 10))
    story.append(Paragraph(format_markdown_for_pdf(resume_analysis), body_style))
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=15))

    # ---------------- Section 2: Career Advice ---------------- #
    story.append(create_section_header("💼 CAREER ADVICE", "#2563EB"))
    story.append(Spacer(1, 10))
    story.append(Paragraph(format_markdown_for_pdf(career_advice), body_style))
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=15))

    # ---------------- Section 3: Resume Improvement ---------------- #
    story.append(create_section_header("💡 RESUME IMPROVEMENT SUGGESTIONS", "#2563EB"))
    story.append(Spacer(1, 10))
    story.append(Paragraph(format_markdown_for_pdf(resume_improvement), body_style))
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=15))

    # ---------------- Section 4: Professional Resume ---------------- #
    story.append(create_section_header("🏆 PROFESSIONAL RESUME", "#2563EB"))
    story.append(Spacer(1, 10))
    story.append(Paragraph(format_markdown_for_pdf(rewritten_resume), body_style))

    doc.build(story)