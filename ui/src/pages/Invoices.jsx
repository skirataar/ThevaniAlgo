import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getInvoices, saveInvoice, getMSMEs, getBuyers, getEvents } from '../data/storage'
import { exportToCSV } from '../data/storage'

export default function Invoices() {
  const navigate = useNavigate()
  const [invoices, setInvoices] = useState([])
  const [msmes, setMsmes] = useState([])
  const [buyers, setBuyers] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    invoiceId: '',
    msmeId: '',
    invoiceDate: new Date().toISOString().split('T')[0],
    amount: '',
    paymentTerms: ''
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = () => {
    setInvoices(getInvoices())
    setMsmes(getMSMEs())
    setBuyers(getBuyers())
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!formData.invoiceId.trim() || !formData.msmeId) return
    
    saveInvoice(formData)
    loadData()
    setFormData({
      invoiceId: '',
      msmeId: '',
      invoiceDate: new Date().toISOString().split('T')[0],
      amount: '',
      paymentTerms: ''
    })
    setShowForm(false)
  }

  const handleExport = () => {
    exportToCSV(invoices, 'invoices.csv')
  }

  const getMSMEName = (msmeId) => {
    const msme = msmes.find(m => m.id === msmeId)
    return msme ? msme.name : '-'
  }

  const getBuyerName = (buyerId) => {
    const buyer = buyers.find(b => b.id === buyerId)
    return buyer ? buyer.name : '-'
  }

  const getLastEvent = (invoiceId) => {
    const events = getEvents(invoiceId)
    return events.length > 0 ? events[events.length - 1] : null
  }

  const calculateDueDate = (invoiceDate, paymentTerms) => {
    if (!invoiceDate || !paymentTerms) return ''
    const date = new Date(invoiceDate)
    date.setDate(date.getDate() + parseInt(paymentTerms))
    return date.toISOString().split('T')[0]
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Invoices</h2>
        <div className="flex space-x-2">
          <button
            onClick={handleExport}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            Export CSV
          </button>
          <button
            onClick={() => setShowForm(!showForm)}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md"
          >
            {showForm ? 'Cancel' : 'Create Invoice'}
          </button>
        </div>
      </div>

      {showForm && (
        <div className="mb-6 p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Invoice ID *
              </label>
              <input
                type="text"
                required
                value={formData.invoiceId}
                onChange={(e) => setFormData({ ...formData, invoiceId: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                MSME *
              </label>
              <select
                required
                value={formData.msmeId}
                onChange={(e) => setFormData({ ...formData, msmeId: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Select MSME</option>
                {msmes.map((msme) => (
                  <option key={msme.id} value={msme.id}>
                    {msme.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Invoice Date *
              </label>
              <input
                type="date"
                required
                value={formData.invoiceDate}
                onChange={(e) => setFormData({ ...formData, invoiceDate: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Invoice Amount *
              </label>
              <input
                type="number"
                step="0.01"
                required
                value={formData.amount}
                onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Payment Terms (days) *
              </label>
              <input
                type="number"
                required
                value={formData.paymentTerms}
                onChange={(e) => setFormData({ ...formData, paymentTerms: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md"
            >
              Save
            </button>
          </form>
        </div>
      )}

      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Invoice ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Buyer
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                MSME
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Amount
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Due Date
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Last Event
              </th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            {invoices.length === 0 ? (
              <tr>
                <td colSpan="6" className="px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400">
                  No invoices yet. Create one to get started.
                </td>
              </tr>
            ) : (
              invoices.map((invoice) => {
                const lastEvent = getLastEvent(invoice.id)
                return (
                  <tr
                    key={invoice.id}
                    onClick={() => navigate(`/invoices/${invoice.id}`)}
                    className="hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer"
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600 dark:text-blue-400">
                      {invoice.invoiceId}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {getBuyerName(invoice.buyerId)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {getMSMEName(invoice.msmeId)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      ₹{invoice.amount.toLocaleString('en-IN')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {invoice.dueDate || calculateDueDate(invoice.invoiceDate, invoice.paymentTerms)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {lastEvent ? (
                        <span>
                          {lastEvent.eventType.replace(/_/g, ' ')} - {lastEvent.eventDate}
                        </span>
                      ) : (
                        <span className="text-gray-400">No events</span>
                      )}
                    </td>
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

