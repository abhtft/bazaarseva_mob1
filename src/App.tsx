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

  const addItem = () => {
    setItems([...items, emptyItem]);
  };

  const submitShoppingList = async (shoppingList: FormInputs[]) => {
    console.log("📤 Sending shopping list to Flask server:", shoppingList);

    try {
      const response = await fetch('/api', {  // Use relative path
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