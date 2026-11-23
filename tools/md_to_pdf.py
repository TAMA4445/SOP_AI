#!/usr/bin/env python3
"""
tools/md_to_pdf.py
Mengonversi seluruh file Markdown SOP di data/sop_md/ menjadi dokumen PDF
berstandar industri di data/sop_sintetis/.

Fitur:
- Teks vektor murni yang dapat diseleksi dan dicari (selectable & searchable text).
- Running Header: Menampilkan Kode SOP, Dokumen ID, dan Judul SOP.
- Running Footer: Menampilkan nama instansi dan penomoran dinamis "Halaman X dari Y".
- Pemformatan Markdown lengkap: Heading, Tabel bergaris & berselang-seling,
  Code block monospace, List bernomor & bullet, serta penekanan teks (bold/italic/code).
"""

import os
import re
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Preformatted, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Dua lintasan (two-pass) canvas untuk menghitung total halaman secara dinamis
    serta menggambar running header dan footer pada setiap halaman.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#334155"))

        page_w, page_h = A4
        margin_x = 18 * mm
        header_y = page_h - 12 * mm
        footer_y = 10 * mm

        doc_code = getattr(self, "doc_code", "SOP K3")
        doc_title = getattr(self, "doc_title", "Standar Operasional Prosedur")

        # --- Running Header ---
        self.drawString(margin_x, header_y, f"{doc_code} | {doc_title}")
        self.setFont("Helvetica", 7.5)
        self.drawRightString(page_w - margin_x, header_y, "SOP K3LH INDUSTRI MANUFAKTUR")
        
        # Garis batas header
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(margin_x, header_y - 2 * mm, page_w - margin_x, header_y - 2 * mm)

        # --- Running Footer ---
        self.line(margin_x, footer_y + 3.5 * mm, page_w - margin_x, footer_y + 3.5 * mm)
        self.drawString(margin_x, footer_y, "PT Industri Presisi Nusantara — Dokumen Terkendali Internal")
        
        page_str = f"Halaman {self._pageNumber} dari {total_pages}"
        self.drawRightString(page_w - margin_x, footer_y, page_str)

        self.restoreState()


def load_sop_catalog(catalog_md_path: Path):
    """Membaca data/daftar_sop.md untuk mendapatkan pemetaan kode dan judul SOP."""
    catalog = {}
    if not catalog_md_path.exists():
        return catalog
    
    with open(catalog_md_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("|") and not line.startswith("| No") and not line.startswith("|---"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 6:
                    kode = parts[2]
                    judul = parts[3]
                    nama_file = parts[4].replace("`", "")
                    stem = Path(nama_file).stem
                    catalog[stem] = {"kode": kode, "judul": judul, "pdf": nama_file}
    return catalog


def format_inline_markdown(text: str) -> str:
    """Mengonversi inline markdown menjadi tag XML yang didukung ReportLab Paragraph."""
    text = text.replace("&", "&amp;")
    # Inline code `code`
    text = re.sub(r'`([^`]+)`', r'<font face="Courier" color="#0F172A"><b>\1</b></font>', text)
    # Bold **text** atau __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
    # Italic *text* atau _text_
    text = re.sub(r'\*([^*]+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_([^_]+?)_', r'<i>\1</i>', text)
    return text


def parse_markdown_to_flowables(md_content: str, styles: dict, content_width: float):
    """Mem-parsing teks Markdown menjadi daftar ReportLab Flowables."""
    flowables = []
    lines = md_content.splitlines()
    
    in_code_block = False
    code_block_lines = []
    
    in_table = False
    table_lines = []

    def flush_table():
        nonlocal in_table, table_lines
        if not table_lines:
            return
        
        rows = []
        for t_line in table_lines:
            if re.match(r'^\s*\|?\s*:?-+:?\s*(\|?\s*:?-+:?\s*)+\|?\s*$', t_line):
                continue
            raw_cols = [c.strip() for c in t_line.strip().strip('|').split('|')]
            rows.append(raw_cols)
        
        if rows:
            col_count = max(len(r) for r in rows)
            normalized_rows = []
            for r_idx, r in enumerate(rows):
                norm_row = []
                for c_idx in range(col_count):
                    val = r[c_idx] if c_idx < len(r) else ""
                    is_header = (r_idx == 0)
                    style = styles["TableHeader"] if is_header else styles["TableCell"]
                    formatted_val = format_inline_markdown(val)
                    formatted_val = formatted_val.replace("<br>", "<br/>")
                    norm_row.append(Paragraph(formatted_val, style))
                normalized_rows.append(norm_row)
            
            if col_count == 2:
                col_widths = [content_width * 0.28, content_width * 0.72]
            elif col_count == 5:
                col_widths = [content_width * 0.20, content_width * 0.23, content_width * 0.27, content_width * 0.15, content_width * 0.15]
            elif col_count == 6:
                col_widths = [content_width * 0.08, content_width * 0.15, content_width * 0.16, content_width * 0.35, content_width * 0.13, content_width * 0.13]
            else:
                col_widths = [content_width / col_count] * col_count
            
            t = Table(normalized_rows, colWidths=col_widths, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
            ]))
            flowables.append(Spacer(1, 1.5 * mm))
            flowables.append(t)
            flowables.append(Spacer(1, 2 * mm))
        
        table_lines = []
        in_table = False

    def flush_code_block():
        nonlocal in_code_block, code_block_lines
        if code_block_lines:
            code_text = "\n".join(code_block_lines)
            p = Preformatted(code_text, styles["CodeBlock"])
            box_table = Table([[p]], colWidths=[content_width])
            box_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0F172A")),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#334155")),
            ]))
            flowables.append(Spacer(1, 1.5 * mm))
            flowables.append(box_table)
            flowables.append(Spacer(1, 2 * mm))
            code_block_lines = []
        in_code_block = False

    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith("```"):
            if in_table:
                flush_table()
            if in_code_block:
                flush_code_block()
            else:
                in_code_block = True
            continue
        
        if in_code_block:
            code_block_lines.append(line)
            continue
        
        if "|" in line and (line.startswith("|") or line.strip().startswith("|")):
            in_table = True
            table_lines.append(line)
            continue
        elif in_table:
            flush_table()

        if not stripped:
            continue

        if re.match(r'^(-{3,}|\*{3,})$', stripped):
            flowables.append(Spacer(1, 1 * mm))
            flowables.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#CBD5E1"), spaceBefore=1, spaceAfter=2))
            continue

        if stripped.startswith("# "):
            title_text = format_inline_markdown(stripped[2:])
            flowables.append(Paragraph(title_text, styles["DocTitle"]))
            continue
        elif stripped.startswith("## "):
            title_text = format_inline_markdown(stripped[3:])
            flowables.append(Paragraph(title_text, styles["DocSubtitle"]))
            continue
        elif stripped.startswith("### "):
            title_text = format_inline_markdown(stripped[4:])
            flowables.append(Paragraph(title_text, styles["HeadingSection"]))
            continue
        elif stripped.startswith("#### "):
            title_text = format_inline_markdown(stripped[5:])
            flowables.append(Paragraph(title_text, styles["HeadingSubSection"]))
            continue

        if re.match(r'^[-*]\s+', stripped):
            item_text = re.sub(r'^[-*]\s+', '', stripped)
            formatted_item = format_inline_markdown(item_text)
            bullet_html = f"&bull; &nbsp; {formatted_item}"
            flowables.append(Paragraph(bullet_html, styles["BulletItem"]))
            continue

        num_match = re.match(r'^(\d+\.)\s+(.+)$', stripped)
        if num_match:
            prefix = num_match.group(1)
            item_text = num_match.group(2)
            formatted_item = format_inline_markdown(item_text)
            list_html = f"<b>{prefix}</b> &nbsp; {formatted_item}"
            flowables.append(Paragraph(list_html, styles["ListItem"]))
            continue

        if stripped.startswith(">"):
            quote_text = stripped.lstrip(">").strip()
            formatted_quote = format_inline_markdown(quote_text)
            quote_p = Paragraph(f"<i>{formatted_quote}</i>", styles["BlockQuote"])
            quote_box = Table([[quote_p]], colWidths=[content_width])
            quote_box.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LINEBEFORE', (0, 0), (0, -1), 2.5, colors.HexColor("#2563EB")),
            ]))
            flowables.append(quote_box)
            continue

        formatted_line = format_inline_markdown(stripped)
        flowables.append(Paragraph(formatted_line, styles["NormalText"]))

    if in_table:
        flush_table()
    if in_code_block:
        flush_code_block()

    return flowables


def build_pdf_styles():
    """Membangun stylesheet profesional untuk dokumen SOP PDF."""
    base = getSampleStyleSheet()

    styles = {
        "DocTitle": ParagraphStyle(
            "DocTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=3,
            spaceAfter=2,
        ),
        "DocSubtitle": ParagraphStyle(
            "DocSubtitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=colors.HexColor("#1E3A8A"),
            spaceBefore=2,
            spaceAfter=2,
        ),
        "HeadingSection": ParagraphStyle(
            "HeadingSection",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=colors.HexColor("#0F2942"),
            spaceBefore=3,
            spaceAfter=1.5,
            keepWithNext=True,
        ),
        "HeadingSubSection": ParagraphStyle(
            "HeadingSubSection",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#1E293B"),
            spaceBefore=2.5,
            spaceAfter=1,
            keepWithNext=True,
        ),
        "NormalText": ParagraphStyle(
            "NormalText",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor("#1E293B"),
            spaceAfter=2,
            alignment=4,  # Justified
        ),
        "BulletItem": ParagraphStyle(
            "BulletItem",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            leftIndent=10,
            firstLineIndent=-10,
            textColor=colors.HexColor("#1E293B"),
            spaceAfter=1.5,
        ),
        "ListItem": ParagraphStyle(
            "ListItem",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            leftIndent=12,
            firstLineIndent=-12,
            textColor=colors.HexColor("#1E293B"),
            spaceAfter=1.5,
        ),
        "BlockQuote": ParagraphStyle(
            "BlockQuote",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.5,
            textColor=colors.HexColor("#1E40AF"),
        ),
        "CodeBlock": ParagraphStyle(
            "CodeBlock",
            parent=base["Normal"],
            fontName="Courier",
            fontSize=7,
            leading=8.5,
            textColor=colors.HexColor("#E2E8F0"),
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9.5,
            textColor=colors.white,
            alignment=0,
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=8.8,
            textColor=colors.HexColor("#0F172A"),
            alignment=0,
        ),
    }
    return styles


def convert_md_to_pdf(md_path: Path, output_pdf_path: Path, catalog: dict):
    """Mengonversi satu file markdown ke PDF dengan running header/footer."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    stem = md_path.stem
    meta = catalog.get(stem, {})
    doc_code = meta.get("kode", "")
    doc_title = meta.get("judul", "")

    if not doc_code:
        match_code = re.search(r'\*\*Nomor Dokumen:\*\*\s*([A-Za-z0-9\-]+)', md_text)
        doc_code = match_code.group(1) if match_code else "SOP-01"

    if not doc_title:
        match_title = re.search(r'^##\s+(.+)$', md_text, re.MULTILINE)
        if match_title:
            doc_title = match_title.group(1).strip()
        else:
            doc_title = "PROSEDUR LOTO"

    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    page_width, page_height = A4
    margin_x = 18 * mm
    margin_top = 18 * mm
    margin_bottom = 16 * mm
    content_width = page_width - (2 * margin_x)

    styles = build_pdf_styles()
    flowables = parse_markdown_to_flowables(md_text, styles, content_width)

    class CustomCanvas(NumberedCanvas):
        pass

    CustomCanvas.doc_code = doc_code
    CustomCanvas.doc_title = doc_title

    doc = SimpleDocTemplate(
        str(output_pdf_path),
        pagesize=A4,
        leftMargin=margin_x,
        rightMargin=margin_x,
        topMargin=margin_top,
        bottomMargin=margin_bottom,
    )

    doc.build(flowables, canvasmaker=CustomCanvas)
    print(f"[OK] Berhasil membuat PDF: {output_pdf_path} ({doc_code} - {doc_title})")


def main():
    root_dir = Path(__file__).resolve().parent.parent
    sop_md_dir = root_dir / "data" / "sop_md"
    sop_pdf_dir = root_dir / "data" / "sop_sintetis"
    catalog_md = root_dir / "data" / "daftar_sop.md"

    if not sop_md_dir.exists():
        print(f"Error: Folder {sop_md_dir} tidak ditemukan.")
        sys.exit(1)

    catalog = load_sop_catalog(catalog_md)
    md_files = list(sop_md_dir.glob("*.md"))

    if not md_files:
        print(f"Tidak ada file .md ditemukan di {sop_md_dir}")
        return

    print(f"Ditemukan {len(md_files)} file SOP Markdown di {sop_md_dir}:")
    for md_file in md_files:
        out_pdf_name = f"{md_file.stem}.pdf"
        out_pdf = sop_pdf_dir / out_pdf_name
        convert_md_to_pdf(md_file, out_pdf, catalog)

    print("\nSeluruh konversi selesai.")


if __name__ == "__main__":
    main()
