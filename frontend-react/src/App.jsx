import { useState, useEffect } from 'react'
import axios from 'axios'
import { Activity, DollarSign, AlertOctagon, RefreshCcw } from 'lucide-react'

function App() {
  const [status, setStatus] = useState(null)
  const [positions, setPositions] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    setLoading(true)
    try {
      const statRes = await axios.get('http://127.0.0.1:8000/api/status')
      setStatus(statRes.data)
      const posRes = await axios.get('http://127.0.0.1:8000/api/positions')
      setPositions(posRes.data)
    } catch (error) {
      console.error("Error fetching data:", error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 10000) // refresh every 10s
    return () => clearInterval(interval)
  }, [])

  const handlePanicKill = async () => {
    if (window.confirm("Are you sure you want to LIQUIDATE ALL POSITIONS instantly?")) {
      try {
        await axios.post('http://127.0.0.1:8000/api/emergency_kill')
        alert("Panic Kill Executed. All positions liquidated.")
        fetchData()
      } catch (e) {
        alert("Failed to execute Panic Kill.")
      }
    }
  }

  return (
    <div className="min-h-screen p-8 max-w-7xl mx-auto">
      <header className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3">
            <Activity className="text-blue-500" size={32} />
            QuantAlgo Trading Bot
          </h1>
          <p className="text-slate-400 mt-2">Swing Trading Strategy Engine (Paper Mode)</p>
        </div>
        
        <div className="flex gap-4">
          <button 
            onClick={fetchData} 
            className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors"
          >
            <RefreshCcw size={16} className={loading ? "animate-spin" : ""} />
            Refresh
          </button>
          <button 
            onClick={handlePanicKill}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg transition-colors shadow-lg shadow-red-900/50"
          >
            <AlertOctagon size={18} />
            EMERGENCY LIQUIDATE
          </button>
        </div>
      </header>

      {/* Account Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <p className="text-slate-400 mb-1 flex items-center gap-2"><DollarSign size={16} /> Total Equity</p>
          <h2 className="text-3xl font-bold">${status?.equity?.toLocaleString(undefined, {minimumFractionDigits: 2}) || "0.00"}</h2>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <p className="text-slate-400 mb-1">Buying Power</p>
          <h2 className="text-3xl font-bold">${status?.buying_power?.toLocaleString(undefined, {minimumFractionDigits: 2}) || "0.00"}</h2>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <p className="text-slate-400 mb-1">Broker Status</p>
          <h2 className="text-xl font-bold text-green-400">
            {status ? `Connected (${status.mode.toUpperCase()})` : "Disconnected"}
          </h2>
        </div>
      </div>

      {/* Open Positions Table */}
      <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
        <div className="p-6 border-b border-slate-700">
          <h3 className="text-xl font-bold">Active Open Positions</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-slate-900/50 text-slate-400">
              <tr>
                <th className="p-4">Symbol</th>
                <th className="p-4">Shares</th>
                <th className="p-4">Avg Entry</th>
                <th className="p-4">Current Price</th>
                <th className="p-4">Market Value</th>
                <th className="p-4">Unrealized P&L</th>
              </tr>
            </thead>
            <tbody>
              {positions.length === 0 ? (
                <tr>
                  <td colSpan="6" className="p-8 text-center text-slate-500">
                    No active positions currently held.
                  </td>
                </tr>
              ) : (
                positions.map((pos) => (
                  <tr key={pos.symbol} className="border-b border-slate-700/50 hover:bg-slate-700/20">
                    <td className="p-4 font-bold">{pos.symbol}</td>
                    <td className="p-4">{pos.qty}</td>
                    <td className="p-4">${pos.avg_entry_price.toFixed(2)}</td>
                    <td className="p-4">${pos.current_price.toFixed(2)}</td>
                    <td className="p-4">${pos.market_value.toFixed(2)}</td>
                    <td className={`p-4 font-bold ${pos.unrealized_pl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                      {pos.unrealized_pl >= 0 ? '+' : ''}${pos.unrealized_pl.toFixed(2)} ({pos.unrealized_plpc.toFixed(2)}%)
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default App
