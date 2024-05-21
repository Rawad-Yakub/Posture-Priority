## Posture-Priority
## To run...
* Create and run a virtual environment (ex. `.venv`)
* `pip install -r requirements.txt`
* Make `dontcommit.py` in project directory (not in `pages/` )file with function my_config() returning:
  * (MongoDB) username, (MongoDB) password, (Amazon) s3_key, (Amazon) s3_secret, (OpenAI) GPT_key
* `streamlit run base.py`
  * If compatibility issues arise, try using `pip install my_package=2.0` or `pip install missing_package`
  * Note that certain libraries may depend on specific versions of one another

## Description
* Posture Priority is an AI-powered webapp for users to upload photos of their posture, and receive individualized exercise recommendations. Try it out to have your photo evaluated, and register and log in to track your posture over time.

## Technologies
* Posture Priority is a Python and HTML/CSS application that relies primarily on Streamlit and Amazon S3 (S3FS API) for its framework and database. MongoDB handles searching for images but this is not permanent.
* Posture analysis handled by Mediapipe, and exercise recommendations from OpenAI GPT 3.5 Turbo.

## Dependencies
* Found in requirements.txt, or view the include headers of files.

CSCI 49900 03 5/21/24
