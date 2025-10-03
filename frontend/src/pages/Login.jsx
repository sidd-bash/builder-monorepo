import { useState } from "react";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = e => {
    e.preventDefault();
    // Call backend login API here
    console.log("Logging in:", form);
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-8 border rounded shadow">
      <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
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
          className="w-full p-3 mb-6 border rounded" 
          name="password" 
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />
        <button type="submit" className="w-full bg-indigo-600 text-white p-3 rounded hover:bg-indigo-700">Login</button>
      </form>
    </div>
  );
}
