import streamlit as st
import requests
from streamlit_lottie import st_lottie
import cv2
from simple_facerec import SimpleFacerec
from apicall import add_in_base
from imagesapi import getimages

getimages()

# Load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Hide Streamlit menu & footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Sidebar
st.sidebar.title('Face Recognition App to Find Missing People')
st.sidebar.subheader('Parameters')

app_mode = st.sidebar.selectbox('Choose the App mode', ['Detection Mode', 'Further Process'])

if app_mode == 'Further Process':
    st.markdown("<h1 style='font-family:sans-serif; color:#282c34; font-size: 50px;font-weight:700'>Further Process</h1>", unsafe_allow_html=True)
    st.markdown("After detecting from the webcam, we can retrieve data related to the missing person, including current location and time detected.")
    st.image("assets/navbarscreenshot.PNG")
else:
    use_webcam = st.sidebar.button('Use Webcam')
    st.markdown("<h1 style='font-family:sans-serif; color:#282c34; font-size: 50px;text-align:center;font-weight:700'>Face Recognition App</h1>", unsafe_allow_html=True)

    lottie_url = "https://assets10.lottiefiles.com/packages/lf20_2szpas4y.json"
    lottie_face = load_lottieurl(lottie_url)

    if not use_webcam:
        st_lottie(lottie_face, key='face recognition')
    else:
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("Error: Unable to access the webcam. Please check if it's connected or used by another application.")
            cap.release()
        else:
            sfr = SimpleFacerec()
            sfr.load_encoding_images("images/")

            FRAME_WINDOW = st.image([])  # Create an empty Streamlit image container
            namesset = set()

            while True:
                ret, frame = cap.read()

                if not ret or frame is None:
                    st.error("Error: Unable to capture frame from webcam. Please restart the camera.")
                    break

                # Detect faces
                face_locations, face_names = sfr.detect_known_faces(frame)
                
                for face_loc, name in zip(face_locations, face_names):
                    y1, x2, y2, x1 = face_loc
                    if name != "Unknown" and name not in namesset:
                        namesset.add(name)
                        add_in_base(name)
                        print(name)

                    cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

                # Convert frame to RGB for Streamlit
                newframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW.image(newframe)   

                key = cv2.waitKey(1)
                if key == 27:  # Press ESC to exit
                    break

            cap.release()
            cv2.destroyAllWindows()
