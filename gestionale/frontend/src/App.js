
import React, { useState } from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import Login from './components/Login';
import AdminDashboard from './components/AdminDashboard';
import TableManagement from './components/TableManagement';
import MenuManagement from './components/MenuManagement';
import Payment from './components/Payment';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userType, setUserType] = useState(null);

  return (
    <div className="App">
      <Switch>
        <Route exact path="/login">
          {isLoggedIn ? <Redirect to="/admin" /> : <Login setIsLoggedIn={setIsLoggedIn} setUserType={setUserType} />}
        </Route>
        <Route exact path="/admin">
          {!isLoggedIn ? <Redirect to="/login" /> : <AdminDashboard />}
        </Route>
        <Route path="/table-management">
          {!isLoggedIn ? <Redirect to="/login" /> : <TableManagement />}
        </Route>
        <Route path="/menu-management">
          {!isLoggedIn ? <Redirect to="/login" /> : <MenuManagement />}
        </Route>
        <Route path="/payment">
          <Payment amount={1000} /> {/* Example: $10.00 */}
        </Route>
        <Route path="/">
          <Redirect to="/login" />
        </Route>
      </Switch>
    </div>
  );
}

export default App;
