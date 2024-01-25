"use client"

import { useState, useEffect } from 'react';
import styles from './chart.module.css'
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Chart = () => {
    const [data, setData] = useState([]);
  
    useEffect(() => {
      fetch('http://127.0.0.1:5000/outliers')
        .then(response => response.json())
        .then(data => {
          const parsedData = data.map(item => ({
            name: item[0],
            visit: item[5]
          }));
          const uniqueData = Object.values(parsedData.reduce((acc, curr) => {
            acc[curr.name] = curr;
            return acc;
          }, {}));
          setData(uniqueData);
        })
        .catch(error => console.error('Error:', error));
    }, []);
  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Weekly Recap</h2>
      <ResponsiveContainer width="100%" height="90%">
        <LineChart
          width={500}
          height={300}
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip contentStyle={{background:"#151c2c", border:"none"}}/>
          <Legend />
          <Line type="monotone" dataKey="visit" stroke="#8884d8" strokeDasharray="5 5" />
          <Line type="monotone" dataKey="click" stroke="#82ca9d" strokeDasharray="3 4 5 2" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default Chart