import React from 'react';
import { Link } from 'react-router-dom';

const AdminDashboard = () => {
  return (
    <div>
      <h2>Admin Dashboard</h2>
      <nav>
        <ul>
          <li><Link to="/table-management">Table Management</Link></li>
          <li><Link to="/menu-management">Menu Management</Link></li>
          <li><Link to="/orders">View Orders</Link></li>
        </ul>
      </nav>
    </div>
  );
};

export default AdminDashboard;
