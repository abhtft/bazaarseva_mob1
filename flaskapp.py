from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from bson import ObjectId

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://abhishek:0LiWdFRno2XWIGaP@cluster0-shard-00-00.yanlm.mongodb.net:27017,cluster0-shard-00-01.yanlm.mongodb.net:27017,cluster0-shard-00-02.yanlm.mongodb.net:27017/?ssl=true&replicaSet=atlas-nox15r-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.kirana_shop
collection = db.shopping_lists

# Ensure downloads directory exists
if not os.path.exists('downloads'):
    os.makedirs('downloads')

def generate_bill_number():
    """Generate unique bill number with date prefix"""
    date_prefix = datetime.now().strftime('%Y%m')
    result = db.bill_counter.find_one_and_update(
        {'_id': date_prefix},
        {'$inc': {'sequence': 1}},
        upsert=True,
        return_document=True
    )
    return f"BILL-{date_prefix}-{str(result['sequence']).zfill(4)}"

def generate_pdf(shopping_list, filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=25,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1f4d7e')
    )
    elements.append(Paragraph("Customer Shopping List", title_style))
    
    # Customer Info Table
    customer_data = [
        ['Bill Number:', shopping_list['bill_number']],
        ['Date:', shopping_list['submission_datetime'].strftime('%Y-%m-%d %H:%M')],
        ['Customer Name:', shopping_list['customer_name']],
        ['Favorite Shop:', shopping_list['favorite_shop']]
    ]
    
    page_width = 515.27559  # A4 width minus margins
    customer_table = Table(
        customer_data, 
        colWidths=[page_width * 0.3, page_width * 0.7],
        spaceBefore=10,
        spaceAfter=20
    )
    
    customer_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
    ]))
    elements.append(customer_table)
    
    # Items Table with Index
    table_data = [
        ['#', 'Item Name', 'Brand', 'Quantity', 'Unit', 'Priority', 'Description']
    ]
    
    # Add items to table with index
    for idx, item in enumerate(shopping_list['items'], 1):
        table_data.append([
            str(idx),
            item['item'],
            item.get('brand', ''),
            item.get('quantity', ''),
            item.get('unit', ''),
            item['priority'],
            item.get('description', '')
        ])

    # Adjust column widths to include index
    col_widths = [
        page_width * 0.05,  # Index (#)
        page_width * 0.20,  # Item Name
        page_width * 0.15,  # Brand
        page_width * 0.10,  # Quantity
        page_width * 0.10,  # Unit
        page_width * 0.15,  # Priority
        page_width * 0.25   # Description
    ]
    
    items_table = Table(
        table_data, 
        colWidths=col_widths,
        repeatRows=1,
        spaceBefore=10,
        spaceAfter=20
    )
    
    items_table.setStyle(TableStyle([
        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4d7e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Table body style
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all columns
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        
        # Grid style
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#1f4d7e')),
        
        # Alternate row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    ]))
    elements.append(items_table)
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_RIGHT,
        spaceBefore=50
    )
    footer_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elements.append(Paragraph(footer_text, footer_style))
    
    doc.build(elements)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Generate bill number
        bill_number = generate_bill_number()

        # Create shopping list document
        shopping_list = {
            'bill_number': bill_number,
            'customer_name': request.form.get('customer_name'),
            'favorite_shop': request.form.get('favorite_shop'),
            'submission_datetime': datetime.now(),
            'items': []
        }

        # Add items
        items = request.form.getlist('item[]')
        brands = request.form.getlist('brand[]')
        quantities = request.form.getlist('qty[]')
        units = request.form.getlist('unit[]')
        priorities = request.form.getlist('priority[]')
        descriptions = request.form.getlist('description_text[]')

        for i in range(len(items)):
            if items[i]:
                shopping_list['items'].append({
                    'item': items[i],
                    'brand': brands[i] if i < len(brands) else '',
                    'quantity': quantities[i] if i < len(quantities) else '',
                    'unit': units[i] if i < len(units) else '',
                    'priority': priorities[i] if i < len(priorities) else 'low',
                    'description': descriptions[i] if i < len(descriptions) else ''
                })

        # Save to MongoDB and generate PDF
        result = collection.insert_one(shopping_list)
        if result.inserted_id:
            pdf_filename = f"{bill_number}.pdf"
            pdf_path = os.path.join('downloads', pdf_filename)
            generate_pdf(shopping_list, pdf_path)
            
            # Pass both list_id and bill_number to success page
            return redirect(url_for('success', 
                                  list_id=str(result.inserted_id), 
                                  bill_number=bill_number))
        
        return "Failed to save", 500

    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {str(e)}", 500

@app.route('/success/<list_id>')
def success(list_id):
    bill_number = request.args.get('bill_number')  # Get bill number from URL params
    return render_template('success.html', list_id=list_id, bill_number=bill_number)

@app.route('/download_pdf/<list_id>')
def download_pdf(list_id):
    pdf_filename = f"shopping_list_{list_id}.pdf"
    pdf_path = os.path.join('downloads', pdf_filename)
    return send_file(pdf_path, as_attachment=True, attachment_filename=pdf_filename)

@app.route('/edit/<list_id>')
def edit_form(list_id):
    try:
        # Fetch the document from MongoDB
        shopping_list = collection.find_one({'_id': ObjectId(list_id)})
        if not shopping_list:
            return "Shopping list not found", 404
            
        # Convert ObjectId to string for template
        shopping_list['_id'] = str(shopping_list['_id'])
        return render_template('index.html', data=shopping_list)
    except Exception as e:
        print(f"Error in edit_form: {e}")
        return "Error loading form", 500

@app.route('/save_and_exit/<list_id>')
def save_and_exit(list_id):
    try:
        doc = collection.find_one({'_id': ObjectId(list_id)})
        if not doc:
            return "Document not found", 404

        pdf_filename = f"{doc['bill_number']}.pdf"
        pdf_path = os.path.join('downloads', pdf_filename)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            attachment_filename=pdf_filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f"Error in save_and_exit: {e}")
        return "Error downloading file", 500

if __name__ == '__main__':
    app.run(debug=True)
