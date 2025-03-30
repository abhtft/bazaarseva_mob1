import { useForm, useFieldArray } from 'react-hook-form';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

interface FormInputs {
  items: Array<{
  itemName: string;
  brand: string;
  quantity: string;
  unit: string;
  priority: string;
  description: string;
  }>;
}

const emptyItem = {
  itemName: '',
  brand: '',
  quantity: '',
  unit: '',
  priority: 'low',
  description: ''
};

function App() {
  const { register, control } = useForm<FormInputs>({
    defaultValues: {
      items: [emptyItem]
    }
  });
  
  const { fields, append } = useFieldArray({
    control,
    name: "items"
  });

  const addItem = () => {
    append(emptyItem);
  };

  const generatePDF = () => {
    const doc = new jsPDF();
    
    // Add title
    doc.setFontSize(20);
    doc.text('Shopping List', 105, 15, { align: 'center' });
    
    // Add items table
    const tableData = fields.map((item, index) => [
      index + 1,
      item.itemName,
      item.brand,
      item.quantity,
      item.unit,
      item.priority,
      item.description
    ]);

    (doc as any).autoTable({
      head: [['#', 'Item', 'Brand', 'Quantity', 'Unit', 'Priority', 'Description']],
      body: tableData,
      startY: 25,
      theme: 'grid',
      styles: {
        fontSize: 10,
        cellPadding: 3,
      },
      columnStyles: {
        0: { cellWidth: 10 },
        1: { cellWidth: 30 },
        2: { cellWidth: 25 },
        3: { cellWidth: 20 },
        4: { cellWidth: 20 },
        5: { cellWidth: 25 },
        6: { cellWidth: 'auto' }
      }
    });

    // Save PDF
    doc.save('shopping-list.pdf');
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    generatePDF();
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>Shopping List</h1>
      
      <form onSubmit={handleSubmit}>
        {fields.map((field, index) => (
          <div key={field.id} style={{ 
            marginBottom: '20px', 
            padding: '15px', 
            border: '1px solid #ddd', 
            borderRadius: '5px' 
          }}>
            <h3>Item #{index + 1}</h3>
            <div style={{ display: 'grid', gap: '10px', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
              <input
                {...register(`items.${index}.itemName`)}
                placeholder="Item name"
                style={inputStyle}
              />
              <input
                {...register(`items.${index}.brand`)}
                placeholder="Brand"
                style={inputStyle}
              />
              <input
                {...register(`items.${index}.quantity`)}
                placeholder="Quantity"
                style={inputStyle}
              />
              <input
                {...register(`items.${index}.unit`)}
                placeholder="Unit"
                style={inputStyle}
              />
              <select
                {...register(`items.${index}.priority`)}
                style={inputStyle}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
              <textarea
                {...register(`items.${index}.description`)}
                placeholder="Description"
                style={{ ...inputStyle, gridColumn: '1 / -1' }}
              />
            </div>
          </div>
        ))}
        
        <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
          <button type="button" onClick={addItem} style={buttonStyle}>
            Add Item
          </button>
          <button type="submit" style={{ ...buttonStyle, backgroundColor: '#4CAF50' }}>
            Generate PDF
          </button>
        </div>
            </form>
    </div>
  );
}

const inputStyle = {
  padding: '8px',
  border: '1px solid #ddd',
  borderRadius: '4px',
  fontSize: '14px',
  width: '100%'
};

const buttonStyle = {
  padding: '10px 20px',
  border: 'none',
  borderRadius: '4px',
  backgroundColor: '#2196F3',
  color: 'white',
  cursor: 'pointer',
  fontSize: '14px'
};

export default App; 