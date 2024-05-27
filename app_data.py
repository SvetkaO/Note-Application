import streamlit as st
import json


# Define colors
beige_color = "#F5F5DC"
green_color = "#AFC8AD"

class Note:
    def __init__(self,title, description):
        self.title = title
        self.description = description


class NoteApp:
    def __init__(self):
        self.notes = self.load_notes()


    def load_notes(self):
        try:
            with open("notes.json", "r") as file:
                notes = json.load(file)
                return [Note(note.get("title", ""),note.get("description", ""),) for note in notes]
        except FileNotFoundError:
            return []

    def save_notes(self):
        with open("notes.json", "w") as file:
            json.dump([{"title": note.title, "description": note.description} for note in self.notes], file)




    def add_note(self,title, description):
        new_note = Note(title, description)
        self.notes.append(new_note)
        self.save_notes()


    def delete_note(self, title):
        for note in self.notes:
            if note.title == title:
                self.notes.remove(note)
                self.save_notes()
                return

    def edit_note(self, title, new_title, new_description):
        for note in self.notes:
            if note.title == title:
                note.title = new_title
                note.description = new_description
                self.save_notes()
                return

    def show_notes(self):
        for note in self.notes:
            st.write(f"**Title:** {note.title}")
            st.write(f"**Description:** {note.description}")
            st.write("---")



    def delete_note_from_show_notes(self, title):
        for note in self.notes:
            if note.title == title:
                self.notes.remove(note)
                self.save_notes()
                return




    def search_notes(self, keyword):
        found_notes = [note for note in self.notes if keyword.lower() in note.title.lower() or keyword.lower() in note.description.lower()]
        return found_notes

# Create an instance of the NoteApp
note_app = NoteApp()

# For app Streamlit UI
st.divider()
st.title("◈ Note Application ◈")
st.divider()
st.header("Be productive, and take notes! 🗒️")
st.markdown("*****")

menu = st.selectbox("Menu", ["Add Note", "Show Notes", "Delete Note", "Search Notes"])

if menu == "Add Note":
    st.subheader("Add a New Note")
    title = st.text_area("Title")
    description = st.text_area("Description")
    if st.button("Add", key="add_button", help="Add a new note",):
        note_app.add_note(title, description)
        st.success("Note added successfully!")



elif menu == "Show Notes":
    st.subheader("Show Notes")
    if len(note_app.notes) == 0:
        st.write("No notes available")
    else:
        for i, note in enumerate(note_app.notes):
            with st.expander(f"Edit Note: {note.title}"):
                new_title = st.text_input(f"New Title {i}", value=note.title)
                new_description = st.text_area(f"New Description {i}", value=note.description)
                if st.button(f"Save {i}", key=f"save_button_{i}", help=f"Save changes for {note.title}"):
                    note_app.edit_note(note.title, new_title, new_description)
                    st.success("Note edited successfully!")
        for note in note_app.notes:
            st.write(f"**Title:** {note.title}")
            st.write(f"**Description:** {note.description}")
            if st.button(f"Delete {note.title}"):
                note_app.delete_note_from_show_notes(note.title)
                st.success("Note deleted successfully!")
        st.write("---")



elif menu == "Delete Note":
    st.subheader("Delete a Note")
    if len(note_app.notes) == 0:
        st.write("No notes available")
    else:
        title = [note.title for note in note_app.notes]
        note_to_delete = st.selectbox("Select note to delete", title)
        if st.button("Delete", key="delete_button", help="Delete selected note"):
            note_app.delete_note(note_to_delete)
            st.success("Note deleted successfully!")


elif menu == "Search Notes":
    st.subheader("Search Notes")
    keyword = st.text_input("Enter keyword to search")
    if st.button("Search", key="search_button", help="Search notes by keyword"):
        found_notes = note_app.search_notes(keyword)
        if found_notes:
            st.write("Found notes:")
            for i, note in enumerate(found_notes):
                with st.expander(f"Note {i+1}: {note.title}"):
                    new_title = st.text_input(f"New Title {i}", value=note.title)
                    new_description = st.text_area(f"New Description {i}", value=note.description)
                    if st.button(f"Save {i}", key=f"save_button_{i}", help=f"Save changes for {note.title}"):
                        note_app.edit_note(note.title, new_title, new_description)
                        st.success("Note edited successfully!")
        else:
            st.write("No notes found")


# Set background color
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {green_color};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(" ➪ Organize your thoughts and record important information! ☀︎ ")