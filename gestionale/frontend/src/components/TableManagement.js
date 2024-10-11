import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TableManagement = () => {
  const [tables, setTables] = useState([]);
  const [newTable, setNewTable] = useState({ number: '', seats: '', x_position: '', y_position: '' });

  useEffect(() => {
    fetchTables();
  }, []);

  const fetchTables = async () => {
    try {
      const response = await axios.get('/api/tables/');
      setTables(response.data);
    } catch (error) {
      console.error('Error fetching tables:', error);
    }
  };

  const handleInputChange = (e) => {
    setNewTable({ ...newTable, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/tables/', newTable);
      fetchTables();
      setNewTable({ number: '', seats: '', x_position: '', y_position: '' });
    } catch (error) {
      console.error('Error creating table:', error);
    }
  };

  return (
    <div>
      <h2>Table Management</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          name="number"
          value={newTable.number}
          onChange={handleInputChange}
          placeholder="Table Number"
          required
        />
        <input
          type="number"
          name="seats"
          value={newTable.seats}
          onChange={handleInputChange}
          placeholder="Number of Seats"
          required
        />
        <input
          type="number"
          name="x_position"
          value={newTable.x_position}
          onChange={handleInputChange}
          placeholder="X Position"
          required
        />
        <input
          type="number"
          name="y_position"
          value={newTable.y_position}
          onChange={handleInputChange}
          placeholder="Y Position"
          required
        />
        <button type="submit">Add Table</button>
      </form>
      <ul>
        {tables.map((table) => (
          <li key={table.id}>
            Table {table.number} - Seats: {table.seats}, Position: ({table.x_position}, {table.y_position})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TableManagement;
