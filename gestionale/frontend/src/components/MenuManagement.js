import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MenuManagement = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [newItem, setNewItem] = useState({ name: '', description: '', price: '', image: null });

  useEffect(() => {
    fetchMenuItems();
  }, []);

  const fetchMenuItems = async () => {
    try {
      const response = await axios.get('/api/menu-items/');
      setMenuItems(response.data);
    } catch (error) {
      console.error('Error fetching menu items:', error);
    }
  };

  const handleInputChange = (e) => {
    if (e.target.name === 'image') {
      setNewItem({ ...newItem, image: e.target.files[0] });
    } else {
      setNewItem({ ...newItem, [e.target.name]: e.target.value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    for (const key in newItem) {
      formData.append(key, newItem[key]);
    }
    try {
      await axios.post('/api/menu-items/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      fetchMenuItems();
      setNewItem({ name: '', description: '', price: '', image: null });
    } catch (error) {
      console.error('Error creating menu item:', error);
    }
  };

  return (
    <div>
      <h2>Menu Management</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          value={newItem.name}
          onChange={handleInputChange}
          placeholder="Item Name"
          required
        />
        <textarea
          name="description"
          value={newItem.description}
          onChange={handleInputChange}
          placeholder="Description"
          required
        />
        <input
          type="number"
          name="price"
          value={newItem.price}
          onChange={handleInputChange}
          placeholder="Price"
          step="0.01"
          required
        />
        <input
          type="file"
          name="image"
          onChange={handleInputChange}
          accept="image/*"
          required
        />
        <button type="submit">Add Menu Item</button>
      </form>
      <ul>
        {menuItems.map((item) => (
          <li key={item.id}>
            {item.name} - ${item.price}
            <p>{item.description}</p>
            <img src={item.image} alt={item.name} style={{ width: '100px' }} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MenuManagement;
