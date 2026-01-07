import streamlit as st

# --- 1. Class Song (เก็บข้อมูลและไฟล์เสียงใน Node) ---
class Song:
    def __init__(self, title, artist, audio_file):
        self.title = title
        self.artist = artist
        self.audio_file = audio_file  # สำคัญ: ต้องเก็บไฟล์เสียงไว้ที่นี่เพื่อให้เล่นได้
        self.next_song = None

    def __str__(self):
        return f"{self.title} by {self.artist}"

# --- 2. Class MusicPlaylist (Logic ของคุณ) ---
class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        self.length = 0

    def add_song(self, title, artist, audio_file):
        new_song = Song(title, artist, audio_file)
        if self.head is None:
            self.head = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current.next_song:
                current = current.next_song
            current.next_song = new_song
        self.length += 1

    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song

    def prev_song(self):
        if self.head is None or self.current_song == self.head:
            return
        current = self.head
        while current.next_song != self.current_song:
            current = current.next_song
        self.current_song = current

    def delete_song(self, title):
        if self.head is None: return
        if self.head.title == title:
            if self.current_song == self.head:
                self.current_song = self.head.next_song
            self.head = self.head.next_song
            self.length -= 1
            return
        current = self.head
        prev = None
        while current and current.title != title:
            prev = current
            current = current.next_song
        if current:
            if self.current_song == current:
                self.current_song = current.next_song if current.next_song else prev
            prev.next_song = current.next_song
            self.length -= 1

# --- 3. ส่วนการจัดวางหน้าตา (UI) ให้เหมือนตัวอย่าง ---
st.set_page_config(page_title="Music Playlist App", layout="wide")

if 'playlist' not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

pl = st.session_state.playlist

# แบ่งคอลัมน์ Sidebar และ Main ตามภาพตัวอย่าง
col_sidebar, col_main = st.columns([1, 2])

with col_sidebar:
    st.header("Add New Song")
    new_title = st.text_input("Title")
    new_artist = st.text_input("Artist")
    uploaded_file = st.file_uploader("Upload Audio File (Optional)", type=['mp3', 'wav', 'ogg'])
    
    if st.button("Add Song to Playlist"):
        if new_title and new_artist and uploaded_file:
            pl.add_song(new_title, new_artist, uploaded_file)
            st.rerun()

    st.markdown("--- 🎵")
    st.header("Delete Song")
    del_title = st.text_input("Song Title to Delete")
    if st.button("Delete Song"):
        pl.delete_song(del_title)
        st.rerun()

with col_main:
    st.title("🎶 Music Playlist App")
    
    st.header("Your Current Playlist")
    if pl.head is None:
        st.write("Playlist is empty. Add some songs from the sidebar!")
    else:
        # วนลูปแสดงเพลงใน Linked List
        curr = pl.head
        while curr:
            indicator = "▶️" if curr == pl.current_song else ""
            st.write(f"{indicator} **{curr.title}** - {curr.artist}")
            curr = curr.next_song

    st.markdown("--- 🎵")
    st.header("Playback Controls")
    
    if pl.current_song:
        # ส่วนแสดงเครื่องเล่นเพลงพร้อมไฟล์เสียงจริง
        st.info(f"Now playing: {pl.current_song.title} by {pl.current_song.artist}")
        if pl.current_song.audio_file:
            st.audio(pl.current_song.audio_file)
        
        # ปุ่มควบคุม Next / Previous
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⏪ Previous"):
                pl.prev_song()
                st.rerun()
        with c2:
            st.button("⏯️ Play Current")
        with c3:
            if st.button("Next ⏩"):
                pl.next_song()
                st.rerun()
    else:
        st.warning("Playlist is empty or no song is selected to play.")

    st.markdown("--- 🎵")
    st.write(f"Total songs in playlist: {pl.length} song(s)")
