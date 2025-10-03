import { useState } from "react";

export default function Signup() {
  const [form, setForm] = useState({ username: "", password: "", confirmPassword: "" });

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = e => {
    e.preventDefault();
    if (form.password !== form.confirmPassword) {
      alert("Passwords do not match");
      return;
    }
    // Call backend signup API here
    console.log("Signing up:", form);
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-8 border rounded shadow">
      <h2 className="text-2xl font-bold mb-6 text-center">Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input 
          className="w-full p-3 mb-4 border rounded" 
          name="username" 
          placeholder="Username"
          value={form.username}
          onChange={handleChange}
          required
        />
        <input 
          className="w-full p-3 mb-4 border rounded" 
          name="password" 
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />
        <input 
          className="w-full p-3 mb-6 border rounded" 
          name="confirmPassword" 
          type="password"
          placeholder="Confirm Password"
          value={form.confirmPassword}
          onChange={handleChange}
          required
        />
        <button type="submit" className="w-full bg-indigo-600 text-white p-3 rounded hover:bg-indigo-700">Sign Up</button>
      </form>
    </div>
  );
}
