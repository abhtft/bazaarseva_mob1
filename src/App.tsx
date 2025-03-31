import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

interface FormInputs {
  itemName: string;
  brand: string;
  quantity: string;
  unit: string;
  priority: string;
  description: string;
}

const emptyItem: FormInputs = {
  itemName: '',
  brand: '',
  quantity: '',
  unit: '',
  priority: 'low',
  description: ''
};

function App() {
  const { control, handleSubmit, reset } = useForm<FormInputs>();
  const [items, setItems] = useState<FormInputs[]>([emptyItem]);
  const [showThankYou, setShowThankYou] = useState(false);

  const addItem = () => {
    setItems([...items, emptyItem]);
  };

  const onSubmit = async (data: FormInputs) => {
    await submitShoppingList(items);
    setShowThankYou(true);
  };

  const submitShoppingList = async (shoppingList: FormInputs[]) => {
    console.log("📤 Sending shopping list to Flask server:", shoppingList);

    try {
      const response = await fetch('/api', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(shoppingList),
      });

      console.log("✅ Response received from Flask server:", response);

      if (!response.ok) {
        const errorData = await response.json();
        console.error("❌ Error response from server:", errorData);
      } else {
        const responseData = await response.json();
        console.log("✅ Successfully saved shopping list:", responseData);
      }
    } catch (error) {
      console.error("❌ Error while sending request to Flask server:", error);
    }
  };

  const createNewList = () => {
    setItems([emptyItem]);
    setShowThankYou(false);
    reset();
  };

  if (showThankYou) {
    return <ThankYouPage onNewList={createNewList} />;
  }

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit(onSubmit)}>
        {items.map((item, index) => (
          <div key={index} className="form-group">
            <input
              {...control.register(`items.${index}.itemName`)}
              placeholder="Item Name"
              className="form-control"
            />
            <input
              {...control.register(`items.${index}.brand`)}
              placeholder="Brand"
              className="form-control"
            />
            <input
              {...control.register(`items.${index}.quantity`)}
              placeholder="Quantity"
              className="form-control"
            />
            <input
              {...control.register(`items.${index}.unit`)}
              placeholder="Unit"
              className="form-control"
            />
            <select
              {...control.register(`items.${index}.priority`)}
              className="form-control"
            >
              <option value="low">Low Priority</option>
              <option value="medium">Medium Priority</option>
              <option value="high">High Priority</option>
            </select>
            <input
              {...control.register(`items.${index}.description`)}
              placeholder="Description"
              className="form-control"
            />
          </div>
        ))}
        <button type="button" onClick={addItem} className="add-entry-button">
          Add Another Item
        </button>
        <button type="submit" className="submit-button">
          Submit List
        </button>
      </form>
    </div>
  );
}

const ThankYouPage: React.FC<{ onNewList: () => void }> = ({ onNewList }) => {
  return (
    <div>
      <h2>Thank you for your order!</h2>
      <button onClick={onNewList}>Create New List</button>
    </div>
  );
};

export default App;