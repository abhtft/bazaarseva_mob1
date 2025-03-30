interface ShoppingList {
  billNumber: string;
  date: string;
  customerName: string;
  favoriteShop: string;
  items: Array<{
    itemName: string;
    brand: string;
    quantity: number;
    unit: string;
    priority: string;
    description: string;
  }>;
} 