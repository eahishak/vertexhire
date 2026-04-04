from app import create_app, db
from app.models import User, Job, Application, Company
import os

app = create_app(os.environ.get("FLASK_ENV", "development"))

def seed():
    """Drop everything, recreate, seed companies + jobs + admin."""
    db.drop_all()
    db.create_all()

    # companies — 22 total with SVG-renderable logo initials and brand colors
    companies = [
        Company(name="Stripe",      industry="Fintech",        location="San Francisco, CA", logo_initial="S",  color="#635BFF"),
        Company(name="Notion",      industry="Productivity",   location="San Francisco, CA", logo_initial="N",  color="#191919"),
        Company(name="Figma",       industry="Design Tools",   location="San Francisco, CA", logo_initial="F",  color="#F24E1E"),
        Company(name="Vercel",      industry="Cloud / DevOps", location="Remote",            logo_initial="▲",  color="#171717"),
        Company(name="Anthropic",   industry="AI Research",    location="San Francisco, CA", logo_initial="A",  color="#CC785C"),
        Company(name="Linear",      industry="Dev Tools",      location="Remote",            logo_initial="L",  color="#5E6AD2"),
        Company(name="Airbnb",      industry="Travel / Tech",  location="San Francisco, CA", logo_initial="A",  color="#FF5A5F"),
        Company(name="Coinbase",    industry="Crypto / Web3",  location="Remote",            logo_initial="C",  color="#0052FF"),
        Company(name="Datadog",     industry="Observability",  location="New York, NY",      logo_initial="D",  color="#632CA6"),
        Company(name="Plaid",       industry="Fintech",        location="San Francisco, CA", logo_initial="P",  color="#111111"),
        Company(name="Ramp",        industry="Finance / SaaS", location="New York, NY",      logo_initial="R",  color="#1A1A1A"),
        Company(name="Retool",      industry="Dev Tools",      location="San Francisco, CA", logo_initial="R",  color="#3D5AFE"),
        Company(name="Scale AI",    industry="AI / Data",      location="San Francisco, CA", logo_initial="S",  color="#6C2BD9"),
        Company(name="Brex",        industry="Fintech",        location="San Francisco, CA", logo_initial="B",  color="#F5360A"),
        Company(name="Rippling",    industry="HR / SaaS",      location="San Francisco, CA", logo_initial="Ri", color="#FDB515"),
        Company(name="Palantir",    industry="Data Analytics", location="Denver, CO",        logo_initial="P",  color="#101010"),
        Company(name="OpenAI",      industry="AI Research",    location="San Francisco, CA", logo_initial="O",  color="#10A37F"),
        Company(name="Snowflake",   industry="Data / Cloud",   location="Remote",            logo_initial="S",  color="#29B5E8"),
        Company(name="Databricks",  industry="Data / AI",      location="San Francisco, CA", logo_initial="D",  color="#FF3621"),
        Company(name="Cloudflare",  industry="Security / CDN", location="San Francisco, CA", logo_initial="C",  color="#F38020"),
        Company(name="Google",      industry="Technology",     location="Mountain View, CA", logo_initial="G",  color="#4285F4"),
        Company(name="Microsoft",   industry="Technology",     location="Redmond, WA",       logo_initial="M",  color="#00A4EF"),
    ]
    db.session.add_all(companies)
    db.session.flush()

    # jobs — one per company
    jobs = [
        Job(title="Software Engineer Intern",      role_type="Software Engineering",
            company_id=companies[0].id,  location="San Francisco, CA", work_type="Hybrid",
            experience="Internship",     deadline="2025-05-01",
            description="Build and scale Stripe's core payment infrastructure. Work on APIs used by millions of developers worldwide.",
            skills="Python,Go,PostgreSQL,Redis,REST APIs", salary_min=8000, salary_max=10000),
        Job(title="Product Manager Intern",        role_type="Product Management",
            company_id=companies[1].id,  location="San Francisco, CA", work_type="Hybrid",
            experience="Internship",     deadline="2025-04-20",
            description="Own product initiatives inside Notion's core editor. Collaborate with design and engineering to ship high-impact features.",
            skills="Product Strategy,User Research,Figma,Analytics,Roadmapping", salary_min=7000, salary_max=9000),
        Job(title="Design Engineer",               role_type="Design",
            company_id=companies[2].id,  location="San Francisco, CA", work_type="On-site",
            experience="New Grad",       deadline="2025-05-15",
            description="Bridge design and engineering at Figma. Build the tools that designers use every day.",
            skills="TypeScript,React,CSS,WebGL,Design Systems", salary_min=120000, salary_max=150000),
        Job(title="Frontend Engineer",             role_type="Software Engineering",
            company_id=companies[3].id,  location="Remote",            work_type="Remote",
            experience="New Grad",       deadline="2025-06-01",
            description="Shape the developer experience at Vercel. Work on Next.js, the dashboard, and cutting-edge DX tooling.",
            skills="TypeScript,Next.js,React,Node.js,Tailwind CSS", salary_min=130000, salary_max=160000),
        Job(title="Research Engineer Intern",      role_type="Data / ML",
            company_id=companies[4].id,  location="San Francisco, CA", work_type="On-site",
            experience="Internship",     deadline="2025-04-30",
            description="Work on foundational AI safety research. Contribute to training runs, evals, and interpretability experiments.",
            skills="Python,PyTorch,JAX,Statistics,Machine Learning", salary_min=9000, salary_max=12000),
        Job(title="Backend Engineer",              role_type="Software Engineering",
            company_id=companies[5].id,  location="Remote",            work_type="Remote",
            experience="Entry Level",    deadline="2025-05-20",
            description="Build Linear's sync engine and real-time collaboration infrastructure used by top engineering teams.",
            skills="TypeScript,Node.js,PostgreSQL,GraphQL,WebSockets", salary_min=140000, salary_max=170000),
        Job(title="iOS Engineer Intern",           role_type="Software Engineering",
            company_id=companies[6].id,  location="San Francisco, CA", work_type="Hybrid",
            experience="Internship",     deadline="2025-05-10",
            description="Work on Airbnb's mobile guest experience. Collaborate with design to ship features used by millions of travelers.",
            skills="Swift,SwiftUI,Objective-C,REST APIs,XCTest", salary_min=7500, salary_max=9500),
        Job(title="Blockchain Engineer Intern",    role_type="Software Engineering",
            company_id=companies[7].id,  location="Remote",            work_type="Remote",
            experience="Internship",     deadline="2025-05-05",
            description="Build and maintain Coinbase's trading infrastructure. Work on high-throughput systems handling billions in daily volume.",
            skills="Go,Python,Solidity,PostgreSQL,Kafka", salary_min=8500, salary_max=11000),
        Job(title="Software Engineer, Metrics",    role_type="Software Engineering",
            company_id=companies[8].id,  location="New York, NY",      work_type="Hybrid",
            experience="New Grad",       deadline="2025-06-10",
            description="Join Datadog's metrics ingestion team. Build the pipelines that process trillions of data points every day.",
            skills="Go,Java,Kafka,Cassandra,Kubernetes", salary_min=135000, salary_max=165000),
        Job(title="Data Engineer Intern",          role_type="Data / ML",
            company_id=companies[9].id,  location="San Francisco, CA", work_type="Hybrid",
            experience="Internship",     deadline="2025-04-25",
            description="Build data pipelines that power Plaid's financial data network connecting thousands of banks and fintech apps.",
            skills="Python,SQL,Airflow,Spark,dbt", salary_min=7000, salary_max=9000),
        Job(title="Product Analyst Intern",        role_type="Product Management",
            company_id=companies[10].id, location="New York, NY",      work_type="Hybrid",
            experience="Internship",     deadline="2025-05-12",
            description="Analyze spend and card data to help Ramp customers save more. Work directly with PMs to define and track product metrics.",
            skills="SQL,Python,Tableau,Excel,Product Analytics", salary_min=7500, salary_max=9000),
        Job(title="Full Stack Engineer Intern",    role_type="Software Engineering",
            company_id=companies[11].id, location="San Francisco, CA", work_type="On-site",
            experience="Internship",     deadline="2025-05-08",
            description="Build the internal tools platform at Retool. Help companies replace spreadsheets and custom scripts with powerful apps.",
            skills="React,Node.js,TypeScript,PostgreSQL,GraphQL", salary_min=8000, salary_max=10500),
        Job(title="ML Data Intern",                role_type="Data / ML",
            company_id=companies[12].id, location="San Francisco, CA", work_type="Hybrid",
            experience="Internship",     deadline="2025-04-28",
            description="Label, curate, and evaluate training data for frontier AI models. Work with Scale's data ops and engineering teams.",
            skills="Python,SQL,Data Annotation,Statistics,Pandas", salary_min=6500, salary_max=8500),
        Job(title="Backend Engineer Intern",       role_type="Software Engineering",
            company_id=companies[13].id, location="San Francisco, CA", work_type="Hybrid",
            experience="Internship",     deadline="2025-05-18",
            description="Build Brex's spend management APIs used by thousands of startups. Work on high-reliability financial infrastructure.",
            skills="Elixir,PostgreSQL,GraphQL,REST APIs,Docker", salary_min=8000, salary_max=10000),
        Job(title="Software Engineer, Platform",   role_type="Software Engineering",
            company_id=companies[14].id, location="San Francisco, CA", work_type="Hybrid",
            experience="New Grad",       deadline="2025-06-05",
            description="Build Rippling's HR and payroll automation platform. Work on the systems that manage workforce data for thousands of companies.",
            skills="Python,Ruby on Rails,PostgreSQL,React,Kubernetes", salary_min=130000, salary_max=160000),
        Job(title="Forward Deployed Engineer",     role_type="Software Engineering",
            company_id=companies[15].id, location="New York, NY",      work_type="On-site",
            experience="New Grad",       deadline="2025-05-25",
            description="Work directly with Palantir's largest clients to deploy and customize data analytics platforms in government and enterprise.",
            skills="Java,Python,SQL,React,Data Pipelines", salary_min=125000, salary_max=155000),
        Job(title="Applied AI Engineer Intern",    role_type="Data / ML",
            company_id=companies[16].id, location="San Francisco, CA", work_type="On-site",
            experience="Internship",     deadline="2025-04-22",
            description="Work on OpenAI's applied research team. Help build and evaluate AI systems that are safe, reliable, and genuinely useful.",
            skills="Python,PyTorch,LLMs,Transformers,RLHF", salary_min=10000, salary_max=13000),
        Job(title="Data Engineer",                 role_type="Data / ML",
            company_id=companies[17].id, location="Remote",            work_type="Remote",
            experience="Entry Level",    deadline="2025-06-15",
            description="Build and maintain Snowflake's internal data platform. Work on pipelines that process petabytes of customer analytics data.",
            skills="SQL,Python,Snowflake,dbt,Airflow", salary_min=120000, salary_max=150000),
        Job(title="ML Engineer Intern",            role_type="Data / ML",
            company_id=companies[18].id, location="San Francisco, CA", work_type="Hybrid",
            experience="Internship",     deadline="2025-05-03",
            description="Work on Databricks' ML platform team. Help data scientists and engineers build, train, and deploy models at scale.",
            skills="Python,Spark,MLflow,PyTorch,Scala", salary_min=9000, salary_max=12000),
        Job(title="Security Engineer Intern",      role_type="Software Engineering",
            company_id=companies[19].id, location="San Francisco, CA", work_type="Hybrid",
            experience="Internship",     deadline="2025-05-14",
            description="Help protect Cloudflare's global network. Work on DDoS mitigation, zero-trust security, and edge network tooling.",
            skills="Rust,Go,Linux,Networking,Cryptography", salary_min=8000, salary_max=10500),
        Job(title="Software Engineer Intern",      role_type="Software Engineering",
            company_id=companies[20].id, location="Mountain View, CA", work_type="Hybrid",
            experience="Internship",     deadline="2025-05-20",
            description="Build products used by billions. Google interns work on real teams across Search, YouTube, Maps, Cloud, and more with full ownership of impactful projects.",
            skills="Python,Java,C++,Go,Distributed Systems", salary_min=9000, salary_max=12000),
        Job(title="PM Intern — Microsoft 365",     role_type="Product Management",
            company_id=companies[20].id, location="Mountain View, CA", work_type="Hybrid",
            experience="Internship",     deadline="2025-05-22",
            description="Drive product strategy for Google Workspace tools used by millions of businesses. Define roadmaps, run user research, and ship features at global scale.",
            skills="Product Strategy,SQL,User Research,Data Analysis,Roadmapping", salary_min=8500, salary_max=11000),
        Job(title="Software Engineer Intern",      role_type="Software Engineering",
            company_id=companies[21].id, location="Redmond, WA",       work_type="Hybrid",
            experience="Internship",     deadline="2025-05-18",
            description="Work across Azure, Office, Xbox, or LinkedIn. Microsoft interns are embedded in real teams shipping products to hundreds of millions of users worldwide.",
            skills="C#,TypeScript,Python,Azure,REST APIs", salary_min=8800, salary_max=11500),
        Job(title="Data Scientist Intern",         role_type="Data / ML",
            company_id=companies[21].id, location="Redmond, WA",       work_type="Hybrid",
            experience="Internship",     deadline="2025-05-15",
            description="Apply machine learning and statistical modeling to Microsoft's massive datasets. Drive insights that directly influence product decisions across Bing, Azure AI, and Teams.",
            skills="Python,R,SQL,Azure ML,Power BI,Statistics", salary_min=8500, salary_max=11000),
    ]
    db.session.add_all(jobs)

    # admin account
    admin = User(first_name="Admin", last_name="VertexHire", email="admin@vertexhire.com")
    admin.set_password("admin1234")
    admin.is_admin = True
    db.session.add(admin)

    db.session.commit()
    print("Seeded: companies, jobs, admin account")
    print("Admin login: admin@vertexhire.com / admin1234")


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Job": Job,
            "Application": Application, "Company": Company}


if __name__ == "__main__":
    with app.app_context():
        seed()
    app.run(debug=True)