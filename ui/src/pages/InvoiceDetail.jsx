import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getInvoices, getMSMEs, getBuyers, getEvents, saveEvent } from '../data/storage'
import { exportToCSV } from '../data/storage'

const EVENT_TYPES = [
  'INVOICE_ACKNOWLEDGED',
  'QUERY_RAISED',
  'DISPUTE_RAISED',
  'PARTIAL_PAYMENT',
  'PAYMENT_RECEIVED'
]

export default function InvoiceDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [invoice, setInvoice] = useState(null)
  const [events, setEvents] = useState([])
  const [msme, setMsme] = useState(null)
  const [buyer, setBuyer] = useState(null)
  const [showEventForm, setShowEventForm] = useState(false)
  const [eventFormData, setEventFormData] = useState({
    eventType: '',
    eventDate: new Date().toISOString().split('T')[0],
    note: '',
    proofUrl: ''
  })

  useEffect(() => {
    loadData()
  }, [id])

  const loadData = () => {
    const invoices = getInvoices()
    const foundInvoice = invoices.find(i => i.id === id)
    if (!foundInvoice) {
      navigate('/')
      return
    }
    
    setInvoice(foundInvoice)
    setEvents(getEvents(id))
    
    const msmes = getMSMEs()
    const foundMsme = msmes.find(m => m.id === foundInvoice.msmeId)
    setMsme(foundMsme)
    
    if (foundMsme && foundMsme.linkedBuyerId) {
      const buyers = getBuyers()
      const foundBuyer = buyers.find(b => b.id === foundMsme.linkedBuyerId)
      setBuyer(foundBuyer)
    }
  }

  const handleEventSubmit = (e) => {
    e.preventDefault()
    if (!eventFormData.eventType) return
    
    saveEvent({
      ...eventFormData,
      invoiceId: id
    })
    loadData()
    setEventFormData({
      eventType: '',
      eventDate: new Date().toISOString().split('T')[0],
      note: '',
      proofUrl: ''
    })
    setShowEventForm(false)
  }

  const handleProofUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      // Simple file URL - in production, upload to server
      const reader = new FileReader()
      reader.onload = (event) => {
        setEventFormData({ ...eventFormData, proofUrl: event.target.result })
      }
      reader.readAsDataURL(file)
    }
  }

  const handleExportEvents = () => {
    exportToCSV(events, `invoice-${invoice?.invoiceId}-events.csv`)
  }

  if (!invoice) {
    return <div className="text-center py-8 text-gray-500 dark:text-gray-400">Loading...</div>
  }

  return (
    <div>
      <div className="mb-4">
        <button
          onClick={() => navigate('/')}
          className="text-blue-600 dark:text-blue-400 hover:underline mb-4"
        >
          ← Back to Invoices
        </button>
      </div>

      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Invoice: {invoice.invoiceId}
        </h2>
        
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Invoice ID</label>
              <p className="text-gray-900 dark:text-white font-medium">{invoice.invoiceId}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-500 dark:text-gray-400">MSME</label>
              <p className="text-gray-900 dark:text-white">{msme?.name || '-'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Buyer</label>
              <p className="text-gray-900 dark:text-white">{buyer?.name || '-'}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Invoice Date</label>
              <p className="text-gray-900 dark:text-white">{invoice.invoiceDate}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Amount</label>
              <p className="text-gray-900 dark:text-white font-medium">₹{invoice.amount.toLocaleString('en-IN')}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Payment Terms</label>
              <p className="text-gray-900 dark:text-white">{invoice.paymentTerms} days</p>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Due Date</label>
              <p className="text-gray-900 dark:text-white">{invoice.dueDate || '-'}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white">Events</h3>
        <div className="flex space-x-2">
          <button
            onClick={handleExportEvents}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            Export CSV
          </button>
          <button
            onClick={() => setShowEventForm(!showEventForm)}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md"
          >
            {showEventForm ? 'Cancel' : 'Add Event'}
          </button>
        </div>
      </div>

      {showEventForm && (
        <div className="mb-6 p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg">
          <form onSubmit={handleEventSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Event Type *
              </label>
              <select
                required
                value={eventFormData.eventType}
                onChange={(e) => setEventFormData({ ...eventFormData, eventType: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Select Event Type</option>
                {EVENT_TYPES.map((type) => (
                  <option key={type} value={type}>
                    {type.replace(/_/g, ' ')}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Event Date *
              </label>
              <input
                type="date"
                required
                value={eventFormData.eventDate}
                onChange={(e) => setEventFormData({ ...eventFormData, eventDate: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Note
              </label>
              <textarea
                value={eventFormData.note}
                onChange={(e) => setEventFormData({ ...eventFormData, note: e.target.value })}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Proof Upload
              </label>
              <input
                type="file"
                onChange={handleProofUpload}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
                accept="image/*,.pdf"
              />
            </div>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md"
            >
              Save Event
            </button>
          </form>
        </div>
      )}

      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
        {events.length === 0 ? (
          <div className="p-8 text-center text-sm text-gray-500 dark:text-gray-400">
            No events yet. Add an event to track invoice progress.
          </div>
        ) : (
          <div className="divide-y divide-gray-200 dark:divide-gray-700">
            {events.map((event) => (
              <div key={event.id} className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="text-lg font-medium text-gray-900 dark:text-white">
                      {event.eventType.replace(/_/g, ' ')}
                    </h4>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                      {event.eventDate}
                    </p>
                  </div>
                </div>
                {event.note && (
                  <p className="text-sm text-gray-700 dark:text-gray-300 mt-2">
                    {event.note}
                  </p>
                )}
                {event.proofUrl && (
                  <div className="mt-3">
                    <a
                      href={event.proofUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
                    >
                      View Proof →
                    </a>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

