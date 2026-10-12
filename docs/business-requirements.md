# Business Requirements — Intelligent Support Assistant

## ۱. کاربر سیستم کیست؟

کاربران اصلی سیستم دو گروه هستند:

1. **کارشناسان پشتیبانی (Support Agents)**  
   افرادی که روزانه با مشتریان صحبت می‌کنند و نیاز دارند سریع به اطلاعات مستندات محصول، وضعیت سفارش، پرداخت و تیکت‌ها دسترسی داشته باشند.

2. **مشتریان نهایی (End Customers)** — در نسخه‌های پیشرفته‌تر  
   مشتریانی که از طریق چت‌بات یا پورتال پشتیبانی سوال می‌پرسند (مثلاً درباره نحوه استفاده از API، وضعیت پرداخت، یا ایجاد تیکت).

در این پروژه تمرکز اصلی روی **کارشناسان پشتیبانی** است، اما معماری طوری طراحی می‌شود که بعداً بتوان به مشتری نهایی هم سرویس داد.

---

## ۲. چه مشکلی دارد؟

- پیدا کردن جواب در مستندات طولانی و پراکنده زمان‌بر است.
- برای چک کردن وضعیت مشتری، سفارش یا پرداخت باید بین چند سیستم جابه‌جا شوند.
- اطلاعات ناقص یا اشتباه باعث طولانی شدن مکالمه و نارضایتی مشتری می‌شود.
- دانش سازمانی در ذهن افراد باتجربه گیر کرده و انتقال آن سخت است.
- ایجاد تیکت و ثبت مشکل دستی و مستعد خطا است.

**نتیجه:** زمان پاسخ‌گویی بالا، خطای انسانی بیشتر و تجربه کاربری ضعیف‌تر.

---

## ۳. سیستم چه کارهایی باید انجام دهد؟

### قابلیت‌های اصلی (Must-Have)

| قابلیت | توضیح |
|--------|--------|
| **پاسخ مبتنی بر دانش (RAG)** | از مستندات رسمی (مثلاً Stripe Docs) جواب دقیق با **Citation** بدهد. |
| **حافظه مکالمه** | تاریخچه گفتگو را حفظ کند تا بتواند به سوالات follow-up جواب دهد. |
| **دسترسی به داده‌های کسب‌وکار** | با Toolها اطلاعات مشتری، سفارش و پرداخت را از دیتابیس بخواند. |
| **ایجاد تیکت** | بتواند تیکت پشتیبانی جدید ثبت کند. |
| **تصمیم‌گیری هوشمند (Agent)** | تشخیص دهد سوال دانشی است یا نیاز به Tool دارد و مسیر درست را انتخاب کند. |
| **API** | از طریق FastAPI در دسترس باشد تا بتوان آن را به فرانت‌اند یا سیستم‌های دیگر وصل کرد. |
| **Citation** | منبع دقیق جواب (عنوان سند + لینک یا شناسه) را نشان دهد. |

### قابلیت‌های مهم (Should-Have)

- مدیریت خطا و پاسخ‌های مودبانه وقتی اطلاعات کافی نیست.
- لاگ‌گیری مناسب برای دیباگ و ارزیابی.
- امکان ارزیابی کیفیت با متریک‌های Recall@K و دقت جواب.
- Docker برای اجرای آسان.

---

## ۴. چه کارهایی نباید انجام دهد؟

- **توهم (Hallucination)**: جوابی که در Context یا Toolها وجود ندارد را اختراع نکند. اگر اطلاعات ندارد صریحاً بگوید.
- **دسترسی غیرمجاز**: اطلاعات مشتری دیگری را نشان ندهد یا بدون اعتبارسنجی داده برنگرداند.
- **اجرای دستورات خطرناک**: فقط Toolهای تعریف‌شده را صدا بزند (نه کد دلخواه).
- **پاسخ خارج از حوزه**: سوالات غیرمرتبط با پشتیبانی محصول/سرویس را رد کند یا به مسیر درست هدایت کند.
- **ذخیره اطلاعات حساس بدون کنترل**: کلیدهای API و داده‌های شخصی را در لاگ یا کد hard-code نکند.
- **پاسخ بدون منبع** در سوالات دانشی: همیشه Citation داشته باشد.

---

## ۵. موفقیت را چطور اندازه می‌گیریم؟

### متریک‌های فنی

| متریک | هدف تقریبی | توضیح |
|-------|------------|--------|
| **Recall@K** (مثلاً K=5) | ≥ 0.80 | سند مرتبط در Top-K بازیابی شود. |
| **Answer Relevance** | ≥ 0.75 | جواب با سوال مرتبط باشد (ارزیابی دستی یا LLM-as-Judge). |
| **Faithfulness / Groundedness** | ≥ 0.85 | جواب فقط بر اساس Context باشد و توهم نداشته باشد. |
| **Citation Accuracy** | ≥ 0.90 | منبع اعلام‌شده واقعاً مرتبط باشد. |
| **Tool Call Accuracy** | ≥ 0.90 | Agent درست تشخیص دهد چه موقع از Tool استفاده کند. |
| **Latency (P95)** | < 5 ثانیه | زمان پاسخ برای اکثر درخواست‌ها. |

### متریک‌های کسب‌وکار (در محیط واقعی)

- کاهش متوسط زمان پاسخ کارشناس پشتیبانی
- افزایش نرخ حل مشکل در اولین تماس (First Contact Resolution)
- کاهش تعداد تیکت‌های تکراری
- امتیاز رضایت کاربر (CSAT) از چت‌بات

### نحوه اندازه‌گیری در این پروژه

- ساخت حداقل ۵۰–۸۰ سوال تستی با جواب مورد انتظار و سند مرتبط (فاز ۵)
- محاسبه متریک‌های ساده Retrieval و کیفیت جواب
- ثبت نتایج در `docs/evaluation.md`
- بعد از هر بهبود، مقایسه قبل/بعد

---

## خلاصه یک‌جمله‌ای

> یک دستیار پشتیبانی هوشمند که با ترکیب **RAG** (برای دانش مستندات) و **Tool Calling** (برای داده‌های مشتری/سفارش/تیکت) به کارشناس پشتیبانی کمک می‌کند سریع، دقیق و با منبع معتبر جواب بدهد.

# Business Requirements — Intelligent Support Assistant

## 1. Business Overview

### 1.1 What is the business domain?

The company operates an e-commerce business that sells products online.

### 1.2 What is the main business goal of this project?

The main goal is to reduce the workload of the customer support team and decrease customer waiting time by automatically answering common support questions.

### 1.3 What business problem are we trying to solve?

Customers currently contact human support for questions about orders, payments, delivery, products, and account-related issues. Many of these questions are repetitive and could potentially be handled automatically.

---

## 2. Users

### 2.1 Who will use the system?

The primary users are customers of the online store.

### 2.2 Are there other users?

In the first version, customer-support employees are not direct users of the system. However, the system should be able to escalate complex or unsupported requests to human support.

---

## 3. Customer Problems and Use Cases

### 3.1 What types of questions should the system answer?

The initial scope includes:

* Order status
* Delivery status
* Payment-related problems
* Product information
* Product availability, if the required data is available
* Similar or alternative products
* Simple account-access problems
* Customer's previous support history

### 3.2 What is outside the initial scope?

The initial version should not automatically perform sensitive or transactional operations such as:

* Creating real orders
* Cancelling orders
* Changing payment information
* Changing sensitive customer information

These may be considered in future versions after appropriate authentication, authorization, and business rules are defined.

---

## 4. Data Requirements

### 4.1 What data does the system need?

Potential data sources include:

* Customer information
* Order information
* Product information
* Payment information
* Delivery/shipping information
* Customer support tickets
* Historical support resolutions
* Product reviews
* Product documentation
* Stripe documentation

### 4.2 What happens if required data is unavailable?

The system must not invent information.

If a business requirement requires data that is not currently available, the missing data source must be identified as a **Data Gap**.

Possible solutions include:

* Connecting to an internal API
* Connecting to an internal database
* Connecting to an external service/API
* Creating an appropriate data source
* Using synthetic data only for demonstration purposes
* Removing or postponing the feature

### 4.3 How should historical support tickets be used?

The system may use previous support tickets from the same customer to understand the customer's history and provide more context-aware responses.

---

## 5. Knowledge and RAG Requirements

### 5.1 What information should come from documentation?

The assistant should be able to retrieve relevant information from product and payment documentation, such as Stripe documentation.

### 5.2 Should the LLM answer purely from its own knowledge?

No.

For business-specific information, the system should prioritize trusted business data and retrieved documentation rather than relying solely on the LLM's internal knowledge.

### 5.3 What should happen when the required information cannot be found?

The system should acknowledge that it does not have enough reliable information and, when appropriate, escalate the issue to human support.

---

## 6. Agent and Tool Requirements

### 6.1 Should the system only answer questions or also perform actions?

The initial version is primarily an information and support system.

The assistant may use tools to retrieve information, but sensitive actions such as creating, cancelling, or modifying orders are outside the initial scope.

### 6.2 What tools might the agent need?

Potential tools include:

* Order lookup
* Customer lookup
* Payment lookup
* Product lookup
* Support-ticket lookup
* Knowledge-base search

The exact tools will be determined during technical design.

---

## 7. Human Handoff

### 7.1 When should the system transfer a customer to human support?

Examples include:

* The system cannot find reliable information
* The customer's problem is outside the supported scope
* The request requires a sensitive operation
* The customer explicitly requests human support
* The issue requires manual investigation

### 7.2 Should sentiment analysis be used?

Not automatically.

Sentiment analysis should only be added if there is a defined business requirement for it, such as detecting highly frustrated customers and prioritizing or escalating their cases.

---

## 8. Security and Privacy

### 8.1 What customer information is sensitive?

Customer identity, payment information, account information, order history, and other personally identifiable information may require access control and privacy protection.

### 8.2 Should every customer be allowed to access every order?

No.

The system must verify that a customer is authorized to access the requested information.

### 8.3 What should happen if the customer's identity cannot be verified?

The system should not reveal private order, payment, or account information and should request appropriate verification or escalate to human support.

---

## 9. Business Constraints and Data Gaps

### 9.1 What if a requested feature requires data that we do not have?

The requirement should remain documented, but the missing data source must be identified before implementation.

### 9.2 What if the available dataset does not represent the real business completely?

The limitations must be documented.

For the portfolio implementation, synthetic data may be introduced where necessary, but it must be clearly labeled as synthetic.

The system should not claim to provide real-time or real-world information when the underlying data does not support it.

---

## 10. Success Criteria

### 10.1 How will we know that the project is successful?

Potential business metrics include:

* Reduction in repetitive support requests
* Percentage of customer questions resolved automatically
* Average response time
* Customer satisfaction
* Escalation rate
* Answer accuracy
* Retrieval accuracy
* Rate of unsupported/hallucinated answers

The final metrics should be agreed upon with the business owner.

---

# Questions to Ask a Real Business Owner

When working with a real company, the following questions should be used to discover requirements rather than assuming them.

## Business Goals

1. What business problem are you trying to solve?
2. Why is this problem important now?
3. What is the current process?
4. How much time, money, or human effort does the current process require?
5. What would success look like after implementing the system?

## Users

6. Who will use the system?
7. How frequently will they use it?
8. What are the most common user problems?
9. Which types of users have different requirements?

## Scope

10. What should the system be able to do?
11. What should the system explicitly NOT do?
12. Which features are critical for the first version?
13. Which features can wait for a later version?

## Data

14. What data is required to perform these tasks?
15. Where is this data currently stored?
16. Who owns the data?
17. How frequently is the data updated?
18. Is the data complete and reliable?
19. Are there important data sources that we currently do not have access to?
20. Are there APIs or databases that can provide the missing data?

## AI Behavior

21. When should the AI answer automatically?
22. When should it ask for clarification?
23. When should it refuse to answer?
24. When should it transfer the case to a human?
25. Is it acceptable for the system to make predictions or estimates?
26. What information must the AI never invent?

## Security and Privacy

27. What customer information is sensitive?
28. Who is authorized to access which information?
29. What authentication or verification is required?
30. Are there legal or compliance requirements?

## Operations

31. Does the system only provide information, or should it perform actions?
32. Which actions is the AI allowed to perform?
33. Which actions require human confirmation?
34. What happens when an external service or API is unavailable?

## Success Metrics

35. How will you measure whether the system is successful?
36. What accuracy level is acceptable?
37. How much reduction in human support workload is expected?
38. What response time is acceptable?
39. What level of customer satisfaction is expected?

## Future Growth

40. What additional capabilities might be needed in the future?
41. Is the system expected to support more products, customers, languages, or regions?
42. Are there plans to connect additional business systems later?

