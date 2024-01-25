"use client";

import { useEffect, useState } from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';

const WebSocketExample = () => {
    const [wsData, setWsData] = useState({});
    const [tickers, setTickers] = useState([]);
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        fetch('https://api.binance.com/api/v3/exchangeInfo')
            .then(response => response.json())
            .then(data => {
                const allTickers = data.symbols.map(symbol => symbol.symbol.toLowerCase());
                const usdtTickers = allTickers.filter(ticker => ticker.endsWith('usdt'));
                setTickers(usdtTickers.slice(0, 50)); // Get the first 50 tickers
            })
            .catch(error => console.error('Error:', error));
    }, []);

    useEffect(() => {
        if (tickers.length === 0) return; // Don't open the WebSocket connection if there are no tickers

        // Create the combined stream URL
        const streamUrl = `wss://stream.binance.com:9443/stream?streams=btcusdt@ticker_1h`;
        console.log(streamUrl);

        const ws = new WebSocket(streamUrl);

        ws.onopen = () => {
            console.log('WebSocket is connected');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setWsData(prevData => ({
                ...prevData,
                [data.stream]: data.data,
            }));

            // Update the chart data
            setChartData(prevChartData => [
                ...prevChartData,
                { time: new Date().toLocaleTimeString(), volume: data.data.w, tickername: data.data.s },
            ]);
        };

        return () => {
            ws.close();
        };
    }, [tickers]);

    return (
        <div>
            <h1>Chart:</h1>
            <LineChart width={300} height={100} data={chartData}>
          <Line type="monotone" dataKey="pv" stroke="#8884d8" strokeWidth={2} />
        </LineChart>
            <h1>WebSocket Data:</h1>
            <pre>{JSON.stringify(wsData, null, 2)}</pre>
        </div>
    );
};

export default WebSocketExample;