cd
source .skyscraper_rc
pushd "$WORK_DIR"
source "$VENV_DIR/bin/activate"
echo "----------" $(date) "------------" >> "$LOG_DIR/skyscraper.log"
python hitit.py >> "$LOG_DIR/skyscraper.log"
popd
deactivate
