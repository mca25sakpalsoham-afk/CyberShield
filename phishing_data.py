PHISHING_EXAMPLES = [
    {
    "subject":"Action required: mailbox quota exceeded", 
    "sender":"support@micros0ft-security.example", 
    "body":"Your mailbox will be disabled. Verify your account immediately at http://security-reset.example", 
    "is_phishing":True, 
    "explanation":"Look-alike sender, urgent pressure, and an external link are phishing indicators."
    },

    {
    "subject":"Quarterly security awareness schedule", 
    "sender":"training@company.example", 
    "body":"The security team published next quarter's training calendar on the internal portal.", 
    "is_phishing":False, 
    "explanation":"The sender, tone, and lack of credential request are consistent with a legitimate internal notice."
    },

    {
    "subject":"Payroll update failed", 
    "sender":"payroll-alert@company-pay.example", 
    "body":"Open the attached macro document and re-enter your banking details.", 
    "is_phishing":True, 
    "explanation":"Payroll pressure plus macro attachment and banking request are high-risk indicators."
    },

    {
    "subject":"Important: Verify your bank account immediately",
    "sender":"security-update@hdfcbank-secure.com",
    "body":"We detected unusual activity on your account. Verify your account within 24 hours to avoid suspension.",
    "is_phishing":True,
    "explanation":"Urgency, account suspension threat, and suspicious domain are phishing indicators."
    },

    {
    "subject":"Annual Leave Approval",
    "sender":"hr@company.example",
    "body":"Your annual leave request has been approved. Please review the attached policy document.",
    "is_phishing":False,
    "explanation":"Professional tone, expected sender, and no request for credentials."
    },

    {
    "subject":"Package Delivery Failed",
    "sender":"delivery@amaz0n-track.example",
    "body":"Your package delivery failed. Click here to reschedule and pay a small processing fee.",
    "is_phishing":True,
    "explanation":"Look-alike domain and unexpected payment request are phishing signs."
    },

    {
    "subject":"Security Awareness Training Reminder",
    "sender":"training@company.example",
    "body":"This is a reminder to complete your cybersecurity awareness training before Friday.",
    "is_phishing":False,
    "explanation":"Legitimate internal communication with no suspicious requests."
    },

    {
    "subject":"Your Email Storage Is Full",
    "sender":"support@microsoft-mailverify.example",
    "body":"Your mailbox has exceeded its storage limit. Login now to prevent account deactivation.",
    "is_phishing":True,
    "explanation":"Pressure tactics and credential harvesting attempt."
    },

    {
    "subject":"Meeting Agenda for Monday",
    "sender":"manager@company.example",
    "body":"Attached is the agenda for Monday's team meeting. Please review before the meeting.",
    "is_phishing":False,
    "explanation":"Normal business communication with no suspicious links or urgency."
    }
]