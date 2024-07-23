import streamlit as st
from supabase import create_client, Client
import uuid

# Supabase configuration
url = "https://ggmsabzwvfglwkpiymzg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdnbXNhYnp3dmZnbHdrcGl5bXpnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE3MDE4MDIsImV4cCI6MjAzNzI3NzgwMn0.tTpxh_aQbQWSiHHFPxn5rybFD2yJkl90RhbJQBOmlMI"
supabase: Client = create_client(url, key)

# Function to insert a new job post
def insert_job_post(location, link, description=""):
    data = {
        "id": str(uuid.uuid4()),
        "location": location,
        "link": link,
        "description": description
    }
    supabase.table("job_posts").insert(data).execute()

# Function to get job posts by location
def get_job_posts(location):
    response = supabase.table("job_posts").select("*").eq("location", location).execute()
    return response.data

# Streamlit UI
st.title("Job Vacancies Tracker")

menu = ["Add Job Post", "View Job Posts"]
choice = st.sidebar.selectbox("Menu", menu)

locations = ["Chennai", "Bangalore", "Coimbatore", "Trichy", "Madurai"]

if choice == "Add Job Post":
    st.subheader("Add Job Post")
    location = st.selectbox("Select Location", locations)
    link = st.text_input("Job Post Link")
    description = st.text_area("Description (optional)")

    if st.button("Add"):
        if link:
            insert_job_post(location, link, description)
            st.success("Job post added successfully!")
        else:
            st.error("Job post link is required.")

elif choice == "View Job Posts":
    st.subheader("View Job Posts")
    location = st.selectbox("Select Location to View", locations)
    if st.button("View"):
        posts = get_job_posts(location)
        if posts:
            for post in posts:
                st.write(f"**Link**: {post['link']}")
                if post['description']:
                    st.write(f"**Description**: {post['description']}")
                st.write("---")
        else:
            st.write("No job posts found for this location.")

