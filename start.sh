until curl -s --head https://www.google.com > /dev/null; do
    echo "No internet yet..."
    sleep 5
done

cd /home/jonas/image_sender_3000
git pull
python /home/jonas/image_sender_3000/send.py
