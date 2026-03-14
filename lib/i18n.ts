export type Locale = "ta" | "en"

export const translations = {
  ta: {
    // App
    appName: "கடன் குரல்",
    tagline: "குரல் மூலம் கடன் பதிவு",

    // Login
    phoneNumber: "கைபேசி எண்",
    getOtp: "OTP பெற",
    verifyOtp: "சரிபார்",
    enterOtp: "OTP உள்ளிடவும்",
    otpError: "OTP தவறானது. மீண்டும் முயற்சிக்கவும்",
    languageToggle: "English",

    // Dashboard
    greeting: "வணக்கம்",
    totalCustomers: "மொத்த வாடிக்கையாளர்கள்",
    customersWithDues: "பாக்கி உள்ளவர்கள்",
    totalOutstanding: "மொத்த பாக்கி",
    todaysTransactions: "இன்றைய பரிவர்த்தனை",
    startSpeaking: "பேச தொடங்க",
    addCustomer: "வாடிக்கையாளர் சேர்",
    viewOutstanding: "பாக்கி பார்",
    sendReminder: "நினைவூட்டல்",

    // Voice Overlay
    listening: "கேட்கிறது\u2026",
    customer: "வாடிக்கையாளர்",
    amount: "தொகை",
    type: "வகை",
    credit: "கடன்",
    payment: "செலுத்தம்",
    confirm: "உறுதிப்படுத்து",
    edit: "திருத்து",
    cancel: "ரத்து",
    success: "வெற்றி!",
    creditAdded: "கடன் சேர்க்கப்பட்டது",
    paymentAdded: "செலுத்தம் பதிவு செய்யப்பட்டது",

    // Customers
    searchCustomer: "வாடிக்கையாளர் பெயர் தேட",
    all: "அனைத்தும்",
    withDues: "பாக்கி",
    cleared: "தீர்ந்தது",
    noCustomers: "வாடிக்கையாளர்கள் இல்லை",
    addCredit: "கடன் சேர்",
    addPayment: "செலுத்தம் சேர்",
    pendingAmount: "நிலுவை தொகை",
    customerName: "வாடிக்கையாளர் பெயர்",
    enterPhone: "தொலைபேசி எண்ணை உள்ளிடவும்",
    createCustomer: "சேர்",
    delete: "அழி",
    deleteCustomer: "வாடிக்கையாளர் நீக்கு",
    deleteCustomerConfirm: "இந்த செயலை மீண்டும் மாற்ற முடியாது.",

    // Outstanding
    totalDueAmount: "மொத்த பாக்கி தொகை",
    daysOverdue: "நாட்கள் தாமதம்",
    remind: "நினைவூட்டு",

    // Reports
    monthlyOverview: "மாதாந்திர பார்வை",
    creditVsPayment: "கடன் vs செலுத்தம்",
    outstandingTrend: "பாக்கி போக்கு",
    avgRecoveryTime: "சராசரி மீட்பு நேரம்",
    monthlyCollection: "மாதாந்திர வசூல்",
    downloadPdf: "PDF பதிவிறக்கம்",
    downloadCsv: "CSV பதிவிறக்கம்",
    days: "நாட்கள்",

    // Settings
    shopDetails: "கடை விவரங்கள்",
    shopName: "கடை பெயர்",
    phone: "தொலைபேசி",
    language: "மொழி",
    smsTemplate: "SMS வார்ப்புரு",
    dataManagement: "தரவு மேலாண்மை",
    backup: "காப்புப்பிரதி",
    restore: "மீட்டமை",
    dangerZone: "ஆபத்து பகுதி",
    deleteAllData: "அனைத்து தரவையும் அழி",
    deleteConfirm: "உறுதியாக அழிக்க விரும்புகிறீர்களா?",
    save: "சேமி",

    // Navigation
    home: "முகப்பு",
    customers: "வாடிக்கையாளர்",
    outstanding: "பாக்கி",
    reports: "அறிக்கை",
    settings: "அமைப்பு",

    // States
    loading: "ஏற்றுகிறது...",
    error: "பிழை ஏற்பட்டது",
    retry: "மீண்டும் முயற்சி",
    empty: "தரவு இல்லை",

    // Transaction
    transactionHistory: "பரிவர்த்தனை வரலாறு",
  },
  en: {
    appName: "Kadan Kural",
    tagline: "Voice-based credit tracking",

    phoneNumber: "Phone Number",
    getOtp: "Get OTP",
    verifyOtp: "Verify",
    enterOtp: "Enter OTP",
    otpError: "Invalid OTP. Please try again",
    languageToggle: "தமிழ்",

    greeting: "Hello",
    totalCustomers: "Total Customers",
    customersWithDues: "With Dues",
    totalOutstanding: "Total Outstanding",
    todaysTransactions: "Today's Transactions",
    startSpeaking: "Start Speaking",
    addCustomer: "Add Customer",
    viewOutstanding: "View Outstanding",
    sendReminder: "Send Reminder",

    listening: "Listening\u2026",
    customer: "Customer",
    amount: "Amount",
    type: "Type",
    credit: "Credit",
    payment: "Payment",
    confirm: "Confirm",
    edit: "Edit",
    cancel: "Cancel",
    success: "Success!",
    creditAdded: "Credit added",
    paymentAdded: "Payment recorded",

    searchCustomer: "Search customer name",
    all: "All",
    withDues: "With Dues",
    cleared: "Cleared",
    noCustomers: "No customers found",
    addCredit: "Add Credit",
    addPayment: "Add Payment",
    pendingAmount: "Pending Amount",
    customerName: "Customer Name",
    enterPhone: "Enter phone number",
    createCustomer: "Create",
    delete: "Delete",
    deleteCustomer: "Delete customer",
    deleteCustomerConfirm: "This action cannot be undone.",

    totalDueAmount: "Total Due Amount",
    daysOverdue: "days overdue",
    remind: "Remind",

    monthlyOverview: "Monthly Overview",
    creditVsPayment: "Credit vs Payment",
    outstandingTrend: "Outstanding Trend",
    avgRecoveryTime: "Avg Recovery Time",
    monthlyCollection: "Monthly Collection",
    downloadPdf: "Download PDF",
    downloadCsv: "Download CSV",
    days: "days",

    shopDetails: "Shop Details",
    shopName: "Shop Name",
    phone: "Phone",
    language: "Language",
    smsTemplate: "SMS Template",
    dataManagement: "Data Management",
    backup: "Backup",
    restore: "Restore",
    dangerZone: "Danger Zone",
    deleteAllData: "Delete All Data",
    deleteConfirm: "Are you sure you want to delete all data?",
    save: "Save",

    home: "Home",
    customers: "Customers",
    outstanding: "Outstanding",
    reports: "Reports",
    settings: "Settings",

    loading: "Loading...",
    error: "An error occurred",
    retry: "Retry",
    empty: "No data",

    transactionHistory: "Transaction History",
  },
} as const

export type TranslationKey = keyof typeof translations.ta

export function t(locale: Locale, key: TranslationKey): string {
  return translations[locale][key]
}
