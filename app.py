import streamlit as st
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="Παρακολούθηση Ασθενοφόρων", layout="wide")
st.title("🚑 Κέντρο Παρακολούθησης Ασθενοφόρων")

if "amb" not in st.session_state:
    st.session_state.amb = {
        i: {
            "name": f"Ασθενοφόρο {i}", 
            "crew": "", 
            "origin": "", 
            "dest": "", 
            "target": None, 
            "total_mins": 0, 
            "active": False
        }
        for i in range(1, 5)
    }

@st.fragment(run_every=1.0)
def draw_screen():
    for i in range(1, 5):
        a = st.session_state.amb[i]
        
        with st.container(border=True):
            # --- ΑΝΑΜΟΝΗ (Φόρμα εισαγωγής) ---
            if not a["active"]:
                # Χρησιμοποιούμε 4 στήλες για να στριμώξουμε τα πάντα οριζόντια
                c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
                
                with c1:
                    a["name"] = st.text_input("Όνομα", value=a["name"], key=f"name_{i}")
                    a["crew"] = st.text_input("Πλήρωμα", value=a["crew"], key=f"crew_{i}", placeholder="Ονόματα")
                    
                with c2:
                    a["origin"] = st.text_input("Από πού", key=f"o{i}", placeholder="π.χ. Αγία Όλγα")
                    a["dest"] = st.text_input("Πού", key=f"d{i}", placeholder="π.χ. Ευαγγελισμός")
                    
                with c3:
                    mins = st.number_input("Χρόνος (λεπτά)", min_value=1, max_value=180, value=15, key=f"m{i}")
                    
                with c4:
                    # Κενό διάστημα για να ευθυγραμμιστεί το κουμπί στο κάτω μέρος
                    st.write("") 
                    st.write("")
                    if st.button("▶ Έναρξη", key=f"btn{i}", use_container_width=True, type="primary"):
                        if a["origin"] and a["dest"]:
                            a["total_mins"] = mins
                            a["target"] = datetime.now() + timedelta(minutes=mins)
                            a["active"] = True
                            st.rerun()
                        else:
                            st.warning("Συμπλήρωσε διαδρομή.")
            
            # --- ΕΝΕΡΓΗ ΔΙΑΔΡΟΜΗ (Αντίστροφη μέτρηση) ---
            else:
                # 3 στήλες: Στοιχεία | Μπάρα | Χρόνος
                col_info, col_prog, col_timer = st.columns([2, 1.5, 1.5])
                
                with col_info:
                    st.markdown(f"### 🚑 {a['name']}")
                    if a["crew"]:
                        st.caption(f"👥 {a['crew']}")
                    st.markdown(f"**📍 {a['origin']} ➔ {a['dest']}**")
                    
                with col_prog:
                    st.write("") # Κενό για ευθυγράμμιση
                    st.write("")
                    remaining = max(0, int((a["target"] - datetime.now()).total_seconds()))
                    total_secs = a["total_mins"] * 60
                    prog = 1 - (remaining / total_secs) if total_secs > 0 else 0
                    st.progress(min(max(prog, 0.0), 1.0))
                    
                    if st.button("⏹ Τέλος", key=f"stop{i}", use_container_width=True):
                        a["active"] = False
                        a["target"] = None
                        st.rerun()
                        
                with col_timer:
                    if remaining > 0:
                        m, s = divmod(remaining, 60)
                        st.markdown(
                            f"<div style='font-size: 45px; font-weight: bold; text-align: center; "
                            f"color: #FF4B4B; font-family: monospace; line-height: 1.2;'>{m}:{s:02d}</div>", 
                            unsafe_allow_html=True
                        )
                    else:
                        st.success("✅ Έφτασε!")

draw_screen()