// Simple localStorage-based storage for Shadow Pilot
// No backend needed - everything stored locally

const STORAGE_KEYS = {
  BUYERS: 'thevani_buyers',
  MSMES: 'thevani_msmes',
  INVOICES: 'thevani_invoices',
  EVENTS: 'thevani_events',
  THEME: 'thevani_theme'
};

// Buyers
export const getBuyers = () => {
  const data = localStorage.getItem(STORAGE_KEYS.BUYERS);
  return data ? JSON.parse(data) : [];
};

export const saveBuyer = (buyer) => {
  const buyers = getBuyers();
  const newBuyer = {
    id: buyer.id || `BUYER-${Date.now()}`,
    name: buyer.name,
    industry: buyer.industry || '',
    notes: buyer.notes || '',
    createdAt: buyer.createdAt || new Date().toISOString()
  };
  const existingIndex = buyers.findIndex(b => b.id === newBuyer.id);
  if (existingIndex >= 0) {
    buyers[existingIndex] = newBuyer;
  } else {
    buyers.push(newBuyer);
  }
  localStorage.setItem(STORAGE_KEYS.BUYERS, JSON.stringify(buyers));
  return newBuyer;
};

// MSMEs
export const getMSMEs = () => {
  const data = localStorage.getItem(STORAGE_KEYS.MSMES);
  return data ? JSON.parse(data) : [];
};

export const saveMSME = (msme) => {
  const msmes = getMSMEs();
  const newMSME = {
    id: msme.id || `MSME-${Date.now()}`,
    name: msme.name,
    gstin: msme.gstin || '',
    linkedBuyerId: msme.linkedBuyerId || null,
    notes: msme.notes || '',
    createdAt: msme.createdAt || new Date().toISOString()
  };
  const existingIndex = msmes.findIndex(m => m.id === newMSME.id);
  if (existingIndex >= 0) {
    msmes[existingIndex] = newMSME;
  } else {
    msmes.push(newMSME);
  }
  localStorage.setItem(STORAGE_KEYS.MSMES, JSON.stringify(msmes));
  return newMSME;
};

// Invoices
export const getInvoices = () => {
  const data = localStorage.getItem(STORAGE_KEYS.INVOICES);
  return data ? JSON.parse(data) : [];
};

export const saveInvoice = (invoice) => {
  const invoices = getInvoices();
  const msmes = getMSMEs();
  const msme = msmes.find(m => m.id === invoice.msmeId);
  
  const invoiceDate = invoice.invoiceDate || new Date().toISOString().split('T')[0];
  const paymentTerms = parseInt(invoice.paymentTerms) || 0;
  
  const newInvoice = {
    id: invoice.id || `INV-${Date.now()}`,
    invoiceId: invoice.invoiceId || '',
    msmeId: invoice.msmeId || null,
    buyerId: msme ? msme.linkedBuyerId : null,
    invoiceDate: invoiceDate,
    amount: parseFloat(invoice.amount) || 0,
    paymentTerms: paymentTerms,
    dueDate: invoice.dueDate || calculateDueDate(invoiceDate, paymentTerms),
    createdAt: invoice.createdAt || new Date().toISOString()
  };
  
  const existingIndex = invoices.findIndex(i => i.id === newInvoice.id);
  if (existingIndex >= 0) {
    invoices[existingIndex] = newInvoice;
  } else {
    invoices.push(newInvoice);
  }
  localStorage.setItem(STORAGE_KEYS.INVOICES, JSON.stringify(invoices));
  return newInvoice;
};

function calculateDueDate(invoiceDate, paymentTerms) {
  if (!invoiceDate || !paymentTerms) return '';
  const date = new Date(invoiceDate);
  date.setDate(date.getDate() + paymentTerms);
  return date.toISOString().split('T')[0];
}

// Events
export const getEvents = (invoiceId) => {
  const data = localStorage.getItem(STORAGE_KEYS.EVENTS);
  const allEvents = data ? JSON.parse(data) : [];
  return allEvents.filter(e => e.invoiceId === invoiceId).sort((a, b) => 
    new Date(a.eventDate) - new Date(b.eventDate)
  );
};

export const saveEvent = (event) => {
  const data = localStorage.getItem(STORAGE_KEYS.EVENTS);
  const events = data ? JSON.parse(data) : [];
  const newEvent = {
    id: event.id || `EVT-${Date.now()}`,
    invoiceId: event.invoiceId,
    eventType: event.eventType,
    eventDate: event.eventDate || new Date().toISOString().split('T')[0],
    note: event.note || '',
    proofUrl: event.proofUrl || null,
    createdAt: event.createdAt || new Date().toISOString()
  };
  events.push(newEvent);
  localStorage.setItem(STORAGE_KEYS.EVENTS, JSON.stringify(events));
  return newEvent;
};

// Theme
export const getTheme = () => {
  return localStorage.getItem(STORAGE_KEYS.THEME) || 'light';
};

export const setTheme = (theme) => {
  localStorage.setItem(STORAGE_KEYS.THEME, theme);
};

// CSV Export
export const exportToCSV = (data, filename) => {
  if (!data || data.length === 0) return;
  
  const headers = Object.keys(data[0]);
  const csvContent = [
    headers.join(','),
    ...data.map(row => headers.map(header => {
      const value = row[header];
      return typeof value === 'string' ? `"${value.replace(/"/g, '""')}"` : value;
    }).join(','))
  ].join('\n');
  
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
};

