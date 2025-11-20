import { useState, useEffect } from 'react'
import { useParams } from "react-router-dom";
import './App.css'

function App() {
  const [jobBoard, setJobBoard] = useState([])
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Note: in case od react router
  // const { company } = useParams()

  // Note: in case od path parameter
  // const path_list = location.pathname.split('/')
  // const company = path_list[path_list.length - 1]
  // console.log(company)

  const urlParams = new URLSearchParams(window.location.search);
  const company = urlParams.get("company")

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/api/job-board/${company}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        setJobBoard(result.jobs);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <p>Loading data...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h1>{company}</h1>
      {jobBoard.map((item, index) => (
        <div key={index}>
          <h2>{item.title}</h2>
          <p>{item.descrition}</p>
        </div>
      ))}
    </div>
  );
}

export default App
