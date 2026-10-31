"""Local sample data for Interview Thozhan. Everything here is predefined demo content (no AI, no internet)."""

APP_NAME = "Interview Thozhan"
TAGLINE = "Your Personal AI Interview Companion"
DISCLAIMER = (
    "Scores come from a simple rule-based checker (keyword coverage, detail and structure). "
    "They are practice feedback only - not real AI evaluation and not a hiring assessment."
)

CANDIDATE = {"name": "Madhanraj", "target": "Software Engineer"}

ROLES = ["Java Developer", "Python Developer", "Full Stack Developer", "Data Analyst"]
DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]
INTERVIEW_TYPES = ["Technical", "HR", "Mixed"]
LEVEL = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}


def _q(qid, role, level, topic, question, concepts, example):
    """concepts: list of (label, 'term1|term2|...') - a concept counts if any term appears in the answer."""
    return {
        "id": qid,
        "role": role,
        "level": level,
        "topic": topic,
        "question": question,
        "concepts": [(label, terms.split("|")) for label, terms in concepts],
        "example": example,
    }


QUESTIONS = [
    # ---------------- Java ----------------
    _q("J1", "Java Developer", 1, "OOP", "What is the difference between an abstract class and an interface in Java?",
       [("An abstract class can hold partial implementation", "abstract class|partial|some implemented|concrete method"),
        ("An interface defines a contract / what to do", "contract|interface|only declare|abstract method"),
        ("A class can implement many interfaces but extend only one class", "multiple|many interfaces|only one class|single inheritance"),
        ("Abstract classes can have constructors and instance variables", "constructor|instance variable|state|fields")],
       "An abstract class is a partly built class that can have both implemented and abstract methods, plus fields and constructors. An interface is a contract that only declares what a class must do. A Java class can extend only one class but implement many interfaces, so I use an interface when unrelated classes need the same behaviour."),
    _q("J2", "Java Developer", 1, "Java Basics", "What is the difference between JDK, JRE and JVM?",
       [("JVM runs Java bytecode", "bytecode|byte code|runs|executes"),
        ("JRE = JVM + libraries needed to run programs", "library|libraries|runtime environment|jre"),
        ("JDK includes development tools such as the compiler", "compiler|javac|development kit|tools|develop"),
        ("Java is platform independent", "platform independent|write once|any os|portable")],
       "The JVM executes Java bytecode. The JRE is the JVM plus the standard libraries needed to run a Java program. The JDK is the JRE plus development tools like the javac compiler, so developers install the JDK. Because bytecode runs on any JVM, Java is platform independent."),
    _q("J3", "Java Developer", 1, "OOP", "Explain the four pillars of OOP with simple examples.",
       [("Encapsulation", "encapsulation|private|getter|setter"),
        ("Inheritance", "inheritance|extends|parent|child"),
        ("Polymorphism", "polymorphism|overriding|overloading|many forms"),
        ("Abstraction", "abstraction|hide|abstract")],
       "Encapsulation keeps data private and exposes it through getters and setters. Inheritance lets a Student class extend a Person class and reuse its code. Polymorphism lets one method behave differently, like overriding speak() in Dog and Cat. Abstraction hides internal details and shows only what is needed, like using an interface."),
    _q("J4", "Java Developer", 2, "Collections", "What is the difference between ArrayList and LinkedList?",
       [("ArrayList is backed by a dynamic array", "array|dynamic array|resiz"),
        ("LinkedList uses nodes (doubly linked)", "node|linked|doubly"),
        ("ArrayList has fast random access by index", "random access|index|get(|fast access"),
        ("LinkedList is better for frequent insert/delete", "insert|delete|add and remove|remov")],
       "ArrayList uses a dynamic array, so reading by index is fast, but inserting in the middle is slow because items shift. LinkedList stores nodes linked to each other, so inserting or deleting is cheap once you reach the node, but access by index is slow. I use ArrayList by default and LinkedList for frequent insertions and removals."),
    _q("J5", "Java Developer", 2, "Collections", "How does a HashMap work internally?",
       [("It uses hashCode to find a bucket", "hashcode|hash code|hashing|hash"),
        ("Data is stored in an array of buckets", "bucket|array|index"),
        ("equals() is used to match the exact key", "equals"),
        ("Collisions are handled with a linked list or tree", "collision|linked list|tree")],
       "HashMap calls hashCode() on the key to find a bucket in an internal array. If several keys land in the same bucket, that is a collision, and they are stored in a linked list (or a tree in newer Java versions). equals() is then used to find the exact key. This gives average O(1) get and put."),
    _q("J6", "Java Developer", 3, "Concurrency", "What is the difference between synchronized and volatile in Java?",
       [("synchronized gives mutual exclusion (locking)", "lock|mutual exclusion|one thread|monitor"),
        ("volatile guarantees visibility across threads", "visibility|visible|main memory"),
        ("volatile does not make compound operations atomic", "atomic|count++|compound|race"),
        ("Both relate to thread safety", "thread")],
       "synchronized lets only one thread enter a block at a time using a lock, so it gives both mutual exclusion and visibility. volatile only guarantees that a variable's latest value is visible to all threads from main memory; it does not make operations like count++ atomic. So I use synchronized or AtomicInteger for compound updates and volatile for simple flags."),
    _q("J7", "Java Developer", 3, "Exceptions", "Explain checked vs unchecked exceptions and how you handle them.",
       [("Checked exceptions are verified at compile time", "compile time|compile-time|checked"),
        ("Unchecked exceptions extend RuntimeException", "runtimeexception|runtime exception|unchecked"),
        ("try-catch-finally is used to handle them", "try|catch|finally"),
        ("throws declares an exception to the caller", "throws|throw")],
       "Checked exceptions like IOException must be handled or declared with throws, because the compiler verifies them. Unchecked exceptions extend RuntimeException, like NullPointerException, and are not forced by the compiler. I handle them with try-catch-finally or try-with-resources and never swallow them silently."),
    # ---------------- Python ----------------
    _q("P1", "Python Developer", 1, "Python Basics", "What is the difference between a list and a tuple in Python?",
       [("Lists are mutable", "mutable|can be changed|can change|modify"),
        ("Tuples are immutable", "immutable|cannot be changed|can't be changed|cannot change"),
        ("Tuples are slightly faster / use less memory", "faster|memory|performance"),
        ("Tuples can be dictionary keys because they are hashable", "hashable|dictionary key|dict key|as a key")],
       "A list is mutable, so I can add, remove or change items. A tuple is immutable, so it cannot be changed after creation. Tuples use less memory and are a bit faster, and because they are hashable they can be used as dictionary keys. I use lists for changing data and tuples for fixed data like coordinates."),
    _q("P2", "Python Developer", 1, "Python Basics", "What is a dictionary in Python and when would you use it?",
       [("It stores key-value pairs", "key-value|key value|key and value|pairs"),
        ("Keys must be unique and hashable", "unique|hashable|immutable"),
        ("Lookups are fast (hash table)", "fast|hash|o(1)|constant"),
        ("A real use case", "for example|such as|use case|count|store|lookup")],
       "A dictionary stores key-value pairs, like {'name': 'Ravi', 'age': 21}. Keys must be unique and hashable. Python uses a hash table, so looking up a value by key is very fast. I use dictionaries for things like counting word frequency or storing a student's details."),
    _q("P3", "Python Developer", 1, "Functions", "What are *args and **kwargs in Python?",
       [("*args collects extra positional arguments", "positional|*args|args"),
        ("**kwargs collects keyword arguments", "keyword|**kwargs|kwargs|name=value"),
        ("args is a tuple and kwargs is a dictionary", "tuple|dictionary|dict"),
        ("They make functions flexible", "flexible|any number|variable number|unknown number")],
       "*args lets a function accept any number of positional arguments, collected as a tuple. **kwargs lets it accept any number of keyword arguments, collected as a dictionary. They make functions flexible when I do not know in advance how many arguments will be passed."),
    _q("P4", "Python Developer", 2, "Functions", "What is a decorator in Python?",
       [("A decorator is a function that wraps another function", "wrap|function that takes a function|takes a function|higher-order|higher order"),
        ("It adds behaviour without changing the original code", "without changing|without modifying|add behaviour|add behavior|extra"),
        ("It is applied with the @ syntax", "@|syntax|above the function"),
        ("A practical example such as logging or timing", "logging|timing|authentication|login|cache|for example")],
       "A decorator is a function that takes another function and wraps it to add behaviour without changing its code. We apply it with the @ symbol above the function. For example, I can write a @timer decorator that prints how long a function takes, or a @login_required decorator in a web app."),
    _q("P5", "Python Developer", 2, "Iterators", "What is the difference between a list and a generator?",
       [("A generator produces values lazily, one at a time", "lazy|lazily|one at a time|on demand|on the fly"),
        ("It uses the yield keyword", "yield"),
        ("Generators save memory for large data", "memory|large data|big data"),
        ("A generator can be iterated only once", "once|exhaust|only one time|one time")],
       "A list stores all items in memory, while a generator produces values lazily one at a time using yield. This saves a lot of memory for large data, such as reading a huge file line by line. The trade-off is that a generator can be iterated only once."),
    _q("P6", "Python Developer", 3, "Python Internals", "What is the GIL in Python and how does it affect multithreading?",
       [("GIL = Global Interpreter Lock", "global interpreter lock|gil"),
        ("Only one thread runs Python bytecode at a time", "one thread|single thread|one at a time|bytecode"),
        ("Threads still help I/O-bound tasks", "i/o|io-bound|io bound|network|file"),
        ("Use multiprocessing for CPU-bound work", "multiprocessing|process|cpu-bound|cpu bound")],
       "The GIL, or Global Interpreter Lock, lets only one thread execute Python bytecode at a time in CPython. So threads do not speed up CPU-bound work, but they still help I/O-bound tasks like network calls because the lock is released while waiting. For CPU-bound work I use multiprocessing."),
    _q("P7", "Python Developer", 3, "Python Internals", "How does Python manage memory?",
       [("Reference counting", "reference count|reference counting|refcount"),
        ("A garbage collector handles reference cycles", "garbage collector|garbage collection|gc|cycle"),
        ("Objects live in a private heap", "heap|private heap"),
        ("Memory is freed when the count reaches zero", "zero|freed|deallocat|release")],
       "Python keeps all objects in a private heap and tracks them with reference counting. When an object's count reaches zero, its memory is freed. A garbage collector also runs to clean up reference cycles, where objects refer to each other and the count never reaches zero."),
    # ---------------- Full Stack ----------------
    _q("F1", "Full Stack Developer", 1, "Web Basics", "What happens when you type a URL in the browser and press Enter?",
       [("DNS lookup converts the domain to an IP address", "dns|ip address"),
        ("The browser sends an HTTP/HTTPS request", "http|request"),
        ("The server processes it and sends a response", "server|response"),
        ("The browser renders HTML, CSS and JavaScript", "render|html|display|css")],
       "The browser first uses DNS to convert the domain name into an IP address. It then sends an HTTP or HTTPS request to that server. The server processes the request and sends back a response, usually HTML. Finally, the browser renders the HTML, CSS and JavaScript to show the page."),
    _q("F2", "Full Stack Developer", 1, "Web Basics", "What is the difference between GET and POST requests?",
       [("GET retrieves data", "retrieve|fetch|read|get data"),
        ("POST sends data to the server (in the body)", "send data|body|submit|create"),
        ("GET parameters are visible in the URL", "url|query string|visible"),
        ("GET is safe/idempotent; POST is not", "idempotent|safe|cache|bookmark")],
       "GET is used to retrieve data and its parameters appear in the URL, so it is visible, can be cached and bookmarked. POST sends data in the request body, for example when submitting a login or registration form, and it is used to create or change data. GET should never change data on the server."),
    _q("F3", "Full Stack Developer", 1, "Frontend", "What is the role of HTML, CSS and JavaScript in a web page?",
       [("HTML gives the structure", "structure|content|skeleton"),
        ("CSS handles styling and layout", "style|styling|layout|design|look"),
        ("JavaScript adds behaviour / interactivity", "interactiv|behaviour|behavior|dynamic|logic"),
        ("A simple example", "for example|button|form|such as")],
       "HTML gives the page its structure and content, like headings and buttons. CSS controls the styling and layout, like colours and spacing. JavaScript adds interactivity, for example validating a form or updating the page when a button is clicked."),
    _q("F4", "Full Stack Developer", 2, "APIs", "What is a REST API and what makes it RESTful?",
       [("It exposes resources through URLs", "resource|url|endpoint"),
        ("It uses HTTP methods like GET, POST, PUT, DELETE", "get|post|put|delete|http method"),
        ("It is stateless", "stateless|no state|each request"),
        ("It commonly returns JSON", "json")],
       "A REST API exposes resources, like /students, through URLs. Clients use HTTP methods such as GET, POST, PUT and DELETE to read, create, update and delete them. It is stateless, meaning each request carries all the information needed, and it usually returns data as JSON."),
    _q("F5", "Full Stack Developer", 2, "Databases", "What is the difference between SQL and NoSQL databases?",
       [("SQL databases use tables with a fixed schema", "table|relational|schema|rows"),
        ("NoSQL stores flexible data such as documents", "document|flexible|key-value|json|mongodb"),
        ("SQL supports joins and ACID transactions", "join|acid|transaction"),
        ("NoSQL scales horizontally easily", "scale|horizontal|large")],
       "SQL databases like MySQL store data in tables with a fixed schema and support joins and ACID transactions, so they suit banking or student records. NoSQL databases like MongoDB store flexible documents and scale horizontally, so they suit fast-changing or very large data. I choose based on how structured the data is."),
    _q("F6", "Full Stack Developer", 3, "Security", "How would you secure a web application?",
       [("Authentication and authorization (login, JWT or sessions)", "authentication|authorization|jwt|session|login"),
        ("Hash passwords, never store plain text", "hash|bcrypt|encrypt"),
        ("Prevent SQL injection with parameterized queries", "sql injection|parameterized|prepared"),
        ("Prevent XSS by escaping or sanitizing input", "xss|sanitiz|escape|cross-site"),
        ("Use HTTPS", "https|ssl|tls")],
       "I would use proper authentication with sessions or JWT and check authorization on every request. Passwords are hashed with bcrypt, never stored as plain text. I use parameterized queries to prevent SQL injection and escape user input to prevent XSS. Finally, everything runs over HTTPS."),
    _q("F7", "Full Stack Developer", 3, "Frontend", "What is the difference between state and props in React?",
       [("Props are passed from parent to child", "parent|passed|pass"),
        ("Props are read-only", "read-only|read only|immutable|cannot be changed"),
        ("State is managed inside the component and can change", "state|useState|internal|changes"),
        ("State changes trigger a re-render", "re-render|rerender|update the ui|render again")],
       "Props are values passed from a parent component to a child and they are read-only. State is data owned by the component itself, managed with useState, and it can change over time. When state changes, React re-renders the component to update the UI."),
    # ---------------- Data Analyst ----------------
    _q("D1", "Data Analyst", 1, "SQL", "What is the difference between WHERE and HAVING in SQL?",
       [("WHERE filters rows before grouping", "before grouping|before group|filters rows|row"),
        ("HAVING filters groups after aggregation", "after|group|aggregat"),
        ("HAVING is used with GROUP BY and functions like COUNT or SUM", "count|sum|avg|group by"),
        ("A short example", "for example|select|such as")],
       "WHERE filters individual rows before grouping happens, while HAVING filters groups after aggregation. For example, I use WHERE to keep only 2024 orders, then GROUP BY customer, and HAVING COUNT(*) > 5 to keep customers with more than five orders."),
    _q("D2", "Data Analyst", 1, "SQL", "What are the different types of SQL joins?",
       [("INNER JOIN returns matching rows", "inner|matching|common"),
        ("LEFT JOIN keeps all rows from the left table", "left"),
        ("RIGHT JOIN keeps all rows from the right table", "right"),
        ("FULL JOIN returns all rows from both tables", "full|outer|all rows from both")],
       "An INNER JOIN returns only rows that match in both tables. A LEFT JOIN returns all rows from the left table plus matches from the right, with NULL where there is no match. A RIGHT JOIN is the opposite. A FULL OUTER JOIN returns all rows from both tables."),
    _q("D3", "Data Analyst", 1, "Statistics", "What are mean, median and mode, and when would you prefer the median?",
       [("Mean is the average", "average|mean"),
        ("Median is the middle value", "middle|median"),
        ("Mode is the most frequent value", "most frequent|most common|mode|frequently"),
        ("Median is better with outliers or skewed data", "outlier|skew|extreme")],
       "The mean is the average, the median is the middle value when data is sorted, and the mode is the most frequent value. I prefer the median when data has outliers or is skewed, for example salaries, because a few very high values distort the mean."),
    _q("D4", "Data Analyst", 2, "Data Cleaning", "How do you handle missing values in a dataset?",
       [("First find out how many are missing and why", "identify|check|isnull|count|why|pattern"),
        ("Remove rows or columns if appropriate", "drop|remove|delete"),
        ("Fill (impute) with mean, median or mode", "impute|fill|mean|median|mode"),
        ("Document the decision / check the impact", "document|impact|validate|compare")],
       "First I check how many values are missing and why, because the reason matters. If very few rows are affected I can drop them. Otherwise I impute, using the median for skewed numbers or the mode for categories. I document the choice and check how it changes the results."),
    _q("D5", "Data Analyst", 2, "Visualization", "How do you choose the right chart for your data?",
       [("Bar charts compare categories", "bar|compare|categor"),
        ("Line charts show trends over time", "line|trend|time"),
        ("Scatter plots show relationships", "scatter|relationship|correlation"),
        ("Think about the audience and message", "audience|message|story|simple")],
       "I start from the question and the audience. Bar charts compare categories, line charts show trends over time, and scatter plots show relationships between two numbers. I keep the chart simple so that the main message is clear."),
    _q("D6", "Data Analyst", 3, "Statistics", "What is the difference between correlation and causation?",
       [("Correlation means two variables move together", "move together|related|relationship|correlat"),
        ("Causation means one change causes the other", "cause|causes|causation"),
        ("A third (confounding) variable can explain it", "confound|third variable|hidden|coincidence"),
        ("Experiments such as A/B tests can prove causation", "experiment|a/b|test|control")],
       "Correlation means two variables move together, but causation means a change in one actually causes the change in the other. A hidden third variable can explain a correlation: ice cream sales and drowning both rise in summer. To prove causation, we need controlled experiments such as A/B tests."),
    _q("D7", "Data Analyst", 3, "SQL", "What are window functions in SQL?",
       [("They calculate across related rows without collapsing them", "without collaps|each row|keep|not collapse|related rows"),
        ("They use the OVER clause", "over"),
        ("PARTITION BY defines the groups", "partition"),
        ("Examples such as RANK, ROW_NUMBER, LAG or running totals", "rank|row_number|lag|lead|running total")],
       "Window functions calculate a value across a set of related rows while still returning every row, unlike GROUP BY which collapses them. They use the OVER clause, and PARTITION BY defines the groups. Examples are RANK, ROW_NUMBER, LAG and running totals."),
    # ---------------- HR (common to all roles) ----------------
    _q("H1", "HR", 1, "Self Introduction", "Tell me about yourself.",
       [("Your education", "student|degree|college|b.e|b.tech|bsc|graduat|studying|education"),
        ("Your key skills", "skill|python|java|sql|html|know|learn"),
        ("A project or internship", "project|internship|built|developed|worked"),
        ("Your career goal", "goal|looking for|want to|aspire|career|opportunity")],
       "I am Madhanraj, a final-year Computer Science student. I am comfortable with Python, Java and SQL. I built a student attendance tracker as a project, which taught me to work with databases. I am now looking for a software engineer role where I can learn and contribute."),
    _q("H2", "HR", 1, "Motivation", "Why do you want to work for our company?",
       [("You researched the company", "research|know about|product|mission|company|read about"),
        ("The role matches your skills", "skill|role|position|match|fit"),
        ("What you can contribute", "contribute|add value|help|bring"),
        ("You want to learn and grow", "learn|grow|growth|opportunit")],
       "I read about your products and your focus on helping students, which matches my interests. The role fits my Python and SQL skills, and I believe I can contribute by learning quickly and working hard. I also see a strong chance to grow with good mentors."),
    _q("H3", "HR", 1, "Self Awareness", "What are your strengths and weaknesses?",
       [("Name a clear strength", "strength|good at|strong"),
        ("Back it up with an example", "for example|for instance|such as|when i|in my project"),
        ("Honestly name a real weakness", "weakness|struggle|difficult|find it hard|used to"),
        ("Show how you are improving it", "improv|working on|practice|trying|learn")],
       "My strength is learning quickly. For example, I learned SQL in two weeks to finish my project. My weakness is that I used to hesitate to speak in groups, so I am improving it by practising presentations and mock interviews."),
    _q("H4", "HR", 2, "Problem Solving", "Describe a challenge you faced and how you solved it.",
       [("The situation or problem", "situation|problem|challenge|issue|bug|error"),
        ("The action you took", "i decided|i tried|i did|i searched|action|approach|solved|fixed"),
        ("The result", "result|finally|outcome|worked|successfully|completed"),
        ("What you learned", "learn|lesson|realis|realiz|next time")],
       "In my final-year project, our database kept crashing during a demo (situation). I read the error logs, found that we were not closing connections, and fixed the code (action). The project ran smoothly and we finished on time (result). I learned to always test under load before a demo."),
    _q("H5", "HR", 2, "Teamwork", "Tell me about a time you worked in a team.",
       [("Describe the team and goal", "team|group|project"),
        ("Your specific role", "my role|i was responsible|i handled|i took|my part|i did"),
        ("How you communicated or handled disagreement", "communicat|discuss|conflict|disagree|coordinate|meeting"),
        ("The result", "result|finally|completed|successfully|delivered")],
       "In a four-member college project, I was responsible for the database part. When two teammates disagreed on the design, we discussed it, listed pros and cons, and chose one together. We delivered the project on time and it was selected for the department expo."),
    _q("H6", "HR", 2, "Career Goals", "Where do you see yourself in five years?",
       [("Growing your technical skills", "skill|learn|technical|expert"),
        ("A realistic role growth", "senior|lead|role|responsib"),
        ("Continuous learning", "learning|certif|course|upskill"),
        ("Contributing to the company", "company|team|contribute|organization")],
       "In five years I want to be a strong engineer with solid technical skills, taking on more responsibility like leading small modules. I will keep learning through courses and projects, and I hope to contribute to the company's growth."),
    _q("H7", "HR", 3, "Resilience", "Tell me about a time you failed. What did you learn?",
       [("Describe a real failure honestly", "failed|failure|mistake|did not|didn't|wrong"),
        ("Take responsibility", "my responsibility|i should|i took|my mistake|i realised|i realized"),
        ("What you learned", "learn|lesson"),
        ("What you changed afterwards", "now i|since then|after that|changed|improv|next time")],
       "In my first semester I failed a programming test because I memorised code without understanding it. I took responsibility and started practising by writing programs myself. The lesson I learned is to understand before memorising. Since then I explain concepts in my own words, and I scored well in the next test."),
    _q("H8", "HR", 1, "Questions for Interviewer", "Do you have any questions for us?",
       [("Ask about the team or culture", "team|culture|work environment"),
        ("Ask about training or growth", "training|learning|growth|mentor"),
        ("Ask about success in the role", "expect|success|first|responsib"),
        ("Thank the interviewer", "thank")],
       "Yes. What does a typical day look like for the team? What training and mentoring is available for freshers? And what would success look like in the first three months? Thank you for your time."),
]

# ---------------- Resume analyzer ----------------
SKILLS = {
    "Python": ["python"], "Java": ["java"], "JavaScript": ["javascript", "js"], "TypeScript": ["typescript"],
    "C++": ["c++"], "HTML": ["html", "html5"], "CSS": ["css", "css3"], "React": ["react", "reactjs", "react.js"],
    "Node.js": ["node.js", "nodejs", "node"], "SQL": ["sql", "mysql", "postgresql", "sqlite"],
    "MongoDB": ["mongodb"], "Git": ["git", "github"], "Spring Boot": ["spring boot", "springboot", "spring"],
    "Flask": ["flask"], "Django": ["django"], "REST API": ["rest api", "rest apis", "restful", "rest"],
    "Pandas": ["pandas"], "NumPy": ["numpy"], "Excel": ["excel"], "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"], "Docker": ["docker"], "AWS": ["aws"], "Linux": ["linux"],
    "Machine Learning": ["machine learning", "ml"], "Data Structures": ["data structures", "dsa", "algorithms"],
    "OOP": ["oop", "oops", "object oriented", "object-oriented"],
    "Problem Solving": ["problem solving", "problem-solving"], "Communication": ["communication"],
    "Teamwork": ["teamwork", "team work", "team player"],
}

SKILL_TASKS = {
    "Python": "Solve 5 easy Python problems (lists, dictionaries, loops) and explain each solution aloud.",
    "Java": "Write 3 small Java classes using inheritance and an interface; explain them in your own words.",
    "JavaScript": "Build a tiny to-do list page with HTML + JavaScript and note what each function does.",
    "HTML": "Build a one-page profile in plain HTML and CSS.",
    "CSS": "Style a simple page using flexbox and explain how it works.",
    "React": "Follow a beginner tutorial and build one small component that uses state and props.",
    "Node.js": "Create a tiny Node.js server with two routes and test it in the browser.",
    "SQL": "Practise 10 queries: SELECT, WHERE, GROUP BY, HAVING and JOINs on a sample table.",
    "MongoDB": "Create a collection, insert 5 documents and run simple find queries.",
    "Git": "Create a repository, make 3 commits, create a branch and merge it.",
    "Spring Boot": "Read an introduction to Spring Boot and build a 'hello' REST endpoint.",
    "Flask": "Build a 2-page Flask app and explain how routing works.",
    "Django": "Follow the official Django tutorial's first two parts.",
    "REST API": "Learn GET, POST, PUT, DELETE and design 4 endpoints for a student-records app.",
    "Pandas": "Load a small CSV in pandas and practise filtering, grouping and handling missing values.",
    "NumPy": "Practise creating arrays and doing basic math operations on them.",
    "Excel": "Make a pivot table and 2 charts from a sample dataset.",
    "Power BI": "Build a one-page dashboard from a sample dataset.",
    "Tableau": "Build one bar chart and one line chart from a sample dataset.",
    "Docker": "Read what containers are and write a simple Dockerfile for a small Python app.",
    "AWS": "Read the basics of EC2 and S3 (no paid services needed to learn the concepts).",
    "Linux": "Practise 15 basic commands (ls, cd, grep, chmod, cat) in a terminal.",
    "Machine Learning": "Learn the difference between supervised and unsupervised learning with one simple example.",
    "Data Structures": "Practise arrays, stacks, queues and hash maps; solve 3 easy problems.",
    "OOP": "Explain the four OOP pillars aloud with one real-life example each.",
    "Problem Solving": "Solve 2 easy coding problems daily and explain your thinking step by step.",
    "Communication": "Record yourself answering 'Tell me about yourself' in 60 seconds and listen back.",
    "Teamwork": "Write one short story about teamwork using Situation - Action - Result.",
}

ROLE_DEFAULT_GAPS = {
    "Java Developer": ["OOP", "Collections", "Exception handling"],
    "Python Developer": ["Python basics", "Functions and decorators", "Python internals"],
    "Full Stack Developer": ["Web basics", "REST APIs", "Databases"],
    "Data Analyst": ["SQL", "Statistics", "Data cleaning"],
}

SAMPLE_RESUME = """MADHANRAJ K (SAMPLE RESUME - DEMO DATA)
Career Objective
Aspiring software engineer who enjoys building small applications and learning new technologies.
Education
B.E. Computer Science and Engineering, Sample Engineering College, 2025 (CGPA 7.8)
Higher Secondary, Sample Government Higher Secondary School, 2021
Skills
Python, Java, SQL (MySQL), HTML, CSS, Git, Problem Solving
Projects
Student Attendance Tracker - Python and MySQL desktop application to record daily attendance.
Library Management System - Java OOP project with classes for books, members and loans.
Internship
Sample Web Development Intern (4 weeks) - built static pages using HTML and CSS.
Certifications
Python for Beginners - sample online course certificate
"""

SAMPLE_JD = """Software Engineer (Fresher) - SAMPLE JOB DESCRIPTION
We are looking for a graduate software engineer to join our product team.
Requirements:
- Good knowledge of Python or Java and Object Oriented Programming
- Strong understanding of Data Structures
- Working knowledge of SQL databases
- Experience building REST APIs
- Familiarity with Git and Docker
- Knowledge of Spring Boot is a plus
- Good communication and teamwork skills
"""

# ---------------- Dashboard sample data (clearly labelled in the UI) ----------------
DEMO_SESSIONS = [
    {"label": "Week 1", "role": "Python Developer", "type": "Technical", "difficulty": "Beginner", "score": 4.8, "sample": True},
    {"label": "Week 2", "role": "Python Developer", "type": "Mixed", "difficulty": "Beginner", "score": 5.6, "sample": True},
    {"label": "Week 3", "role": "Python Developer", "type": "Technical", "difficulty": "Intermediate", "score": 6.1, "sample": True},
    {"label": "Week 4", "role": "Java Developer", "type": "Mixed", "difficulty": "Intermediate", "score": 6.9, "sample": True},
]
DEMO_ACTIVITY = [
    "Completed a Mixed mock interview (Java Developer)",
    "Analyzed resume against a Software Engineer job description",
    "Completed 3 of 7 roadmap tasks",
    "Practised the 'Tell me about yourself' answer",
]
DEMO_SKILLS_TO_IMPROVE = ["REST API", "Docker", "Data Structures", "Spring Boot"]

# Canned answers (varying quality) used only by the 'Explore Demo' report. They are scored by the real checker.
DEMO_INTERVIEW_IDS = ["P1", "P4", "H1", "P5", "H4"]
DEMO_ANSWERS = {
    "P1": "A list is mutable so we can change its items, but a tuple is immutable. Tuples are faster and use less memory, so I use them for fixed data. Because tuples are hashable they can be used as dictionary keys.",
    "P4": "A decorator is a function that wraps another function to add behaviour without changing it. We use the @ symbol above the function.",
    "H1": "I am Madhanraj, a final year computer science student. I know Python and Java and I built a small attendance project. I want to start my career as a software engineer.",
    "P5": "Generator is used for loops.",
    "H4": "Once I had a problem in my project database. I solved it.",
}

# ---------------- Career mentor content ----------------
MENTOR_TOPICS = {
    "Java interview preparation": {
        "icon": "☕",
        "en": """**Focus on these Java areas (in this order):**
- **Core basics:** JDK vs JRE vs JVM, data types, `String` immutability, `==` vs `.equals()`.
- **OOP:** the four pillars, abstract class vs interface, overloading vs overriding.
- **Collections:** ArrayList vs LinkedList, HashMap internals, HashSet.
- **Exceptions:** checked vs unchecked, try-catch-finally.
- **Basics of multithreading:** thread vs runnable, `synchronized`.

**Tip:** For every concept, prepare a one-line definition, one example and one real use case.""",
        "ta": """**Java interview-க்கு இந்த வரிசையில் படியுங்கள்:**
- **அடிப்படை:** JDK, JRE, JVM வித்தியாசம், data types, String மாற்ற முடியாதது (immutable), `==` மற்றும் `.equals()` வேறுபாடு.
- **OOP:** நான்கு தூண்கள், abstract class மற்றும் interface வித்தியாசம்.
- **Collections:** ArrayList, LinkedList, HashMap எப்படி வேலை செய்கிறது.
- **Exceptions:** checked மற்றும் unchecked exception, try-catch-finally.
- **Multithreading அடிப்படை:** thread என்றால் என்ன, `synchronized` எதற்கு.

**குறிப்பு:** ஒவ்வொரு concept-க்கும் ஒரு வரி விளக்கம், ஒரு உதாரணம், ஒரு நிஜப் பயன்பாடு என மூன்றையும் தயார் செய்யுங்கள்.""",
        "practice": ["Why is String immutable in Java?", "What is the difference between == and equals()?", "When would you use an interface instead of an abstract class?"],
    },
    "Python interview preparation": {
        "icon": "🐍",
        "en": """**Focus on these Python areas:**
- **Basics:** list vs tuple vs set vs dictionary, mutable vs immutable.
- **Functions:** `*args`, `**kwargs`, lambda, decorators.
- **Iterators:** list comprehensions, generators, `yield`.
- **OOP in Python:** classes, `__init__`, inheritance.
- **Internals:** memory management and the GIL (for stronger candidates).

**Tip:** Be ready to write small programs, such as reversing a string or counting word frequency, and explain them aloud.""",
        "ta": """**Python interview-க்கு இவற்றில் கவனம் செலுத்துங்கள்:**
- **அடிப்படை:** list, tuple, set, dictionary வித்தியாசம்; மாற்றக்கூடியது (mutable) மற்றும் மாற்ற முடியாதது (immutable).
- **Functions:** `*args`, `**kwargs`, lambda, decorator.
- **Iterators:** list comprehension, generator, `yield`.
- **Python-ல் OOP:** class, `__init__`, inheritance.
- **உள்ளமைப்பு:** memory management மற்றும் GIL (மேம்பட்ட நிலைக்கு).

**குறிப்பு:** ஒரு string-ஐ தலைகீழாக மாற்றுவது, வார்த்தைகளை எண்ணுவது போன்ற சிறிய program-களை எழுதி, சத்தமாக விளக்கிப் பழகுங்கள்.""",
        "practice": ["What is the difference between a list and a tuple?", "What does a decorator do?", "Write a function that counts word frequency in a sentence."],
    },
    "OOP concepts": {
        "icon": "🧩",
        "en": """**The four pillars of OOP:**
- **Encapsulation:** keep data and the code that uses it together, and protect the data (like an ATM hiding your PIN).
- **Inheritance:** a child class reuses the features of a parent class (Student inherits from Person).
- **Polymorphism:** the same action behaves differently depending on the object (speak() for Dog vs Cat).
- **Abstraction:** show only what is needed and hide the internal details (you drive a car without knowing how the engine works).

**Interview tip:** Always give a real-life example after the definition.""",
        "ta": """**OOP-ன் நான்கு தூண்கள்:**
- **Encapsulation (உறைபொதிவு):** தகவலையும் அதைப் பயன்படுத்தும் செயல்களையும் ஒரே class-க்குள் வைத்து, தகவலைப் பாதுகாப்பது. உதாரணம்: ATM-ல் உங்கள் PIN வெளியே தெரியாது.
- **Inheritance (மரபுரிமை):** ஒரு class, மற்றொரு class-ன் பண்புகளைப் பெற்றுக்கொள்வது. உதாரணம்: Student, Person-ன் பண்புகளைப் பெறும்.
- **Polymorphism (பல்லுருவம்):** ஒரே செயல், பொருளுக்கு ஏற்ப வெவ்வேறு விதமாக நடப்பது. உதாரணம்: நாய், பூனை இரண்டும் speak() செய்யும்; ஆனால் ஒலி வேறு.
- **Abstraction (சுருக்கம்):** தேவையானதை மட்டும் காட்டி, உள் விவரங்களை மறைப்பது. உதாரணம்: கார் ஓட்ட இன்ஜின் எப்படி வேலை செய்கிறது என்று தெரிய வேண்டியதில்லை.

**Interview குறிப்பு:** வரையறை சொன்ன பிறகு, எப்போதும் ஒரு நிஜ வாழ்க்கை உதாரணம் சொல்லுங்கள்.""",
        "practice": ["Explain encapsulation with a real-life example.", "What is the difference between overloading and overriding?", "Why do we use abstraction?"],
    },
    "SQL interview questions": {
        "icon": "🗄️",
        "en": """**SQL topics that are asked most often:**
- **Basics:** SELECT, WHERE, ORDER BY, LIMIT.
- **Aggregation:** GROUP BY with COUNT, SUM, AVG; WHERE vs HAVING.
- **Joins:** INNER, LEFT, RIGHT, FULL.
- **Keys:** primary key vs foreign key.
- **Next level:** subqueries, indexes, window functions.

**Tip:** Practise on a small sample table. Say aloud which rows each query returns and why.""",
        "ta": """**SQL interview-ல் அதிகம் கேட்கப்படுபவை:**
- **அடிப்படை:** SELECT, WHERE, ORDER BY, LIMIT.
- **கூட்டல் கணக்குகள்:** GROUP BY உடன் COUNT, SUM, AVG; WHERE மற்றும் HAVING வித்தியாசம் (WHERE வரிசைகளை முதலில் வடிகட்டும்; HAVING குழுக்களை வடிகட்டும்).
- **Joins:** INNER, LEFT, RIGHT, FULL.
- **Keys:** primary key (தனித்துவமான அடையாளம்) மற்றும் foreign key (மற்றொரு table-உடன் இணைப்பு).
- **அடுத்த நிலை:** subquery, index, window function.

**குறிப்பு:** சிறிய sample table-ல் பயிற்சி செய்யுங்கள். ஒவ்வொரு query-யும் எந்த வரிசைகளைத் தரும், ஏன் என்று சத்தமாகச் சொல்லுங்கள்.""",
        "practice": ["What is the difference between WHERE and HAVING?", "Explain INNER JOIN and LEFT JOIN.", "What is a primary key?"],
    },
    "HR interview tips": {
        "icon": "🤝",
        "en": """**Simple structure for HR answers:**
- **Tell me about yourself:** education - skills - one project - your goal (about 60 seconds).
- **Strengths/weaknesses:** choose real ones and always add an example or how you are improving.
- **Challenge questions:** use **STAR** - Situation, Task, Action, Result.
- **Why this company:** read the company website for 10 minutes before the interview.
- **Last question:** always ask one thoughtful question about the team or training.

**Remember:** Honest and calm answers are better than perfect-sounding memorised answers.""",
        "ta": """**HR கேள்விகளுக்கு எளிய அமைப்பு:**
- **உங்களைப் பற்றிச் சொல்லுங்கள்:** படிப்பு - திறன்கள் - ஒரு project - உங்கள் இலக்கு (சுமார் 60 விநாடிகள்).
- **பலம்/பலவீனம்:** உண்மையானவற்றைச் சொல்லி, ஒரு உதாரணம் அல்லது எப்படி மேம்படுத்துகிறீர்கள் என்பதைச் சேர்க்கவும்.
- **சவால் பற்றிய கேள்விகள்:** **STAR** முறை - Situation (நிலைமை), Task (பணி), Action (நீங்கள் செய்தது), Result (முடிவு).
- **ஏன் இந்த நிறுவனம்:** interview-க்கு முன் அவர்கள் website-ஐ 10 நிமிடம் படியுங்கள்.
- **கடைசிக் கேள்வி:** குழு அல்லது பயிற்சி பற்றி ஒரு நல்ல கேள்வி கேளுங்கள்.

**நினைவில் வையுங்கள்:** மனப்பாடம் செய்த பதிலை விட, நேர்மையான, அமைதியான பதில் சிறந்தது.""",
        "practice": ["Tell me about yourself.", "Describe a challenge you solved.", "Why should we hire you?"],
    },
    "Resume improvement": {
        "icon": "📄",
        "en": """**Make your resume stronger:**
- Keep it to **one page** with clear headings: Education, Skills, Projects, Internship, Certifications.
- For each project, write **what you built, which tools you used and what the result was**.
- Put the skills from the job description first - but only if you really have them.
- Use action words: built, designed, analysed, improved.
- Check spelling and keep one simple font.

**Never** add skills you cannot explain in an interview.""",
        "ta": """**உங்கள் resume-ஐ வலுவாக்க:**
- **ஒரே பக்கத்தில்** தெளிவான தலைப்புகளுடன் வைக்கவும்: Education, Skills, Projects, Internship, Certifications.
- ஒவ்வொரு project-க்கும் **என்ன உருவாக்கினீர்கள், எந்தக் கருவிகள் பயன்படுத்தினீர்கள், என்ன பலன் கிடைத்தது** என்று எழுதுங்கள்.
- Job description-ல் கேட்கப்பட்ட திறன்களை முதலில் எழுதுங்கள் - ஆனால் உங்களுக்கு உண்மையில் தெரிந்தவற்றை மட்டும்.
- built, designed, analysed, improved போன்ற செயல் சொற்களைப் பயன்படுத்துங்கள்.
- எழுத்துப்பிழை பார்த்து, ஒரே எளிய font பயன்படுத்துங்கள்.

Interview-ல் விளக்க முடியாத திறன்களை **ஒருபோதும்** சேர்க்காதீர்கள்.""",
        "practice": ["Pick one project and describe it in 3 lines: what, how, result.", "List 5 skills you can explain confidently.", "Write 2 action-verb bullet points for your best project."],
    },
    "Communication improvement": {
        "icon": "🎤",
        "en": """**Improve your spoken English step by step:**
- Think in short sentences. A clear short answer beats a long confusing one.
- Practise aloud for 10 minutes every day - record yourself and listen back.
- Use a simple pattern: **Answer first, then reason, then example.**
- It is fine to pause for 3 seconds and think before you answer.
- Technical understanding matters more than accent. Do not worry about your accent.

**Daily habit:** Explain one concept you learned today in 5 sentences.""",
        "ta": """**பேச்சு ஆங்கிலத்தை படிப்படியாக மேம்படுத்த:**
- சிறிய வாக்கியங்களில் சிந்தியுங்கள். நீண்ட குழப்பமான பதிலை விட, தெளிவான சிறிய பதில் சிறந்தது.
- தினமும் 10 நிமிடம் சத்தமாகப் பயிற்சி செய்யுங்கள் - பதிவு செய்து கேளுங்கள்.
- எளிய அமைப்பு: **முதலில் பதில், பிறகு காரணம், பிறகு உதாரணம்.**
- பதில் சொல்லும் முன் 3 விநாடி யோசிப்பது தவறில்லை.
- உச்சரிப்பை விட, தொழில்நுட்பப் புரிதலே முக்கியம். உங்கள் உச்சரிப்பைப் பற்றிக் கவலைப்பட வேண்டாம்.

**தினசரிப் பழக்கம்:** இன்று கற்ற ஒரு concept-ஐ 5 வாக்கியங்களில் விளக்குங்கள்.""",
        "practice": ["Explain what a variable is in 3 sentences.", "Introduce yourself in 60 seconds.", "Explain one project to a friend who is not from IT."],
    },
}
