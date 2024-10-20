// src/app/page.tsx
"use client"
import { useState } from 'react';

export default function Home() {
  const [result, setResult] = useState('');

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const endpoint = formData.get('endpoint') as string;

    try {
      const response = await fetch(`http://localhost:8000${endpoint}`);
      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      setResult(`Error: ${error}`);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">FastAPI Bug Tester</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <select name="endpoint" className="mr-2 p-2 border rounded">
          <option value="/users">Get Users</option>
          <option value="/items">Get Items</option>
          <option value="/process">Process Data</option>
        </select>
        <button type="submit" className="bg-blue-500 text-white p-2 rounded">
          Send Request
        </button>
      </form>
      <pre className="bg-gray-100 p-4 rounded">{result}</pre>
    </div>
  );
}