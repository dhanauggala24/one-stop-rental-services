import { BrowserRouter, Routes, Route } from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import LoginSelector from "./pages/LoginSelector";
import Login from "./pages/Login";
import Register from "./pages/Register";

import UserDashboard from "./pages/UserDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import ForgotPassword from "./pages/ForgotPassword";

import AllItems from "./pages/AllItems";
import Payment from "./pages/Payment";
import CreateItem from "./pages/CreateItem";
import MyBookings from "./pages/MyBookings";
import Cart from "./pages/Cart";
import Receipt from "./pages/Receipt";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />

        <Route path="/login" element={<LoginSelector />} />

        <Route path="/signin" element={<Login />} />

        <Route path="/register" element={<Register />} />

        <Route path="/receipt/:bookingId" element={<Receipt />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />

        <Route
          path="/user-dashboard"
          element={
            <ProtectedRoute allowedRoles={["user"]}>
              <UserDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/admin-dashboard"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/items"
          element={
            <ProtectedRoute allowedRoles={["user", "admin"]}>
              <AllItems />
            </ProtectedRoute>
          }
        />

        <Route
          path="/create-item"
          element={
            <ProtectedRoute allowedRoles={["user"]}>
              <CreateItem />
            </ProtectedRoute>
          }
        />

        <Route
          path="/my-bookings"
          element={
            <ProtectedRoute allowedRoles={["user"]}>
              <MyBookings />
            </ProtectedRoute>
          }
        />
        <Route
  path="/cart"
  element={
    <ProtectedRoute allowedRoles={["user"]}>
      <Cart />
    </ProtectedRoute>
  }
/>
<Route
  path="/payment"
  element={
    <ProtectedRoute allowedRoles={["user"]}>
      <Payment />
    </ProtectedRoute>
  }
/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;