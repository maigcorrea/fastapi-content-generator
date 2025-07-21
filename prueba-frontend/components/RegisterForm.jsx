// RegisterForm.jsx
import { useState } from "react";
import axios from "axios";

export default function RegisterForm() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Form data submitted:", formData);
    try {
        console.log("Sending data to server");
      const res = await axios.post("http://localhost:8000/users", formData);
      console.log("Response from server:");
      alert("Registro exitoso: " + res.data.username);
    } catch (error) {
      console.error(error);
      alert("Error en el registro");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="username" placeholder="Username" onChange={handleChange} required />
      <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
      <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
      <button type="submit">Register</button>
    </form>
  );
}
