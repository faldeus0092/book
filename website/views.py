from flask import Blueprint, flash, render_template, request, flash, redirect, url_for
from .models import  Book, id_to_string
from . import db
import os
from .models import parseCSV
from sqlalchemy import text
import boto3
import key_config as keys

BUCKET_NAME='cc22book'

views = Blueprint('views', __name__)
UPLOAD_FOLDER = 'static/files'
ROOT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), UPLOAD_FOLDER)

# homepage
@views.route('/', methods = ['GET', 'POST'])
def home():
    genre = request.form.get('genre')
    title = request.form.get('title')
    author = request.form.get('author')
    if request.method == 'POST':
        if genre=="0" and not title and not author:
            flash("Please enter search filter(s)", category='error')
            sql = text(f'Select `book`.`judul`, `book`.`author`, `book`.`isbn`, `book`.`genre`, `book`.`img_path` FROM `book`;')  
            results = db.engine.execute(sql)
            return render_template("home.html", results = results)
        # search by genre
        elif not title and not author:
            sql = text(f'Select `book`.`judul`, `book`.`author`, `book`.`isbn`, `book`.`genre`, `book`.`img_path` FROM `book` WHERE `book`.`genre` LIKE \'%{genre}%\';') 
            results = db.engine.execute(sql)
            if results.rowcount == 0:
                flash("Not Found", category='error')
            else:
                flash(f"Found {results.rowcount} results matching genre {genre}", category='success')
            return render_template("home.html", results = results)
        # search by title
        elif genre=="0" and not author:
            sql = text(f'Select `book`.`judul`, `book`.`author`, `book`.`isbn`, `book`.`genre`, `book`.`img_path` FROM `book` WHERE `book`.`judul` LIKE \'%{title}%\';') 
            results = db.engine.execute(sql)
            if results.rowcount == 0:
                flash("Not Found", category='error')
            else:
                flash(f"Found {results.rowcount} results matching title {title}", category='success')
            return render_template("home.html", results = results)
        # search by author
        elif genre=="0" and not title:
            sql = text(f'Select `book`.`judul`, `book`.`author`, `book`.`isbn`, `book`.`genre`, `book`.`img_path` FROM `book` WHERE `book`.`author` LIKE \'%{author}%\';') 
            results = db.engine.execute(sql)
            if results.rowcount == 0:
                flash("Not Found", category='error')
            else:
                flash(f"Found {results.rowcount} results matching author {author}", category='success')
            return render_template("home.html", results = results)
        # search by genre & title
        elif not author and (title and genre != "0"):
            sql = text(f'Select `book`.`judul`, `book`.`author`, `book`.`isbn`, `book`.`genre`, `book`.`img_path` FROM `book` WHERE `book`.`genre` LIKE \'%{genre}%\' AND `book`.`judul` LIKE \'%{title}%\';') 
            results = db.engine.execute(sql)
            if results.rowcount == 0:
                flash("Not Found", category='error')
            else:
                flash(f"Found {results.rowcount} results matching genre {genre} and title {title}", category='success')
            return render_template("home.html", results = results)
        # search by genre & author
        elif not title and (author and genre != "0"):
            sql = text(f'Select `book`.`judul`, `book`.`author`, `book`.`isbn`, `book`.`genre`, `book`.`img_path` FROM `book` WHERE `book`.`genre` LIKE \'%{genre}%\' AND `book`.`author` LIKE \'%{author}%\';') 
            results = db.engine.execute(sql)
            if results.rowcount == 0:
                flash("Not Found", category='error')
            else:
                flash(f"Found {results.rowcount} results matching genre {genre} and author {author}", category='success')
            return render_template("home.html", results = results)
        # search by title & author
        elif genre == "0" and (author and title):
            sql = text(f'Select `book`.`judul`, `book`.`author`, `book`.`isbn`, `book`.`genre`, `book`.`img_path` FROM `book` WHERE `book`.`judul` LIKE \'%{title}%\' AND `book`.`author` LIKE \'%{author}%\';') 
            results = db.engine.execute(sql)
            if results.rowcount == 0:
                flash("Not Found", category='error')
            else:
                flash(f"Found {results.rowcount} results matching title {title} and author {author}", category='success')
            return render_template("home.html", results = results)
        # search by title & author
        elif genre != "0" and author and title:
            sql = text(f'Select `book`.`judul`, `book`.`author`, `book`.`isbn`, `book`.`genre`, `book`.`img_path` FROM `book` WHERE `book`.`judul` LIKE \'%{title}%\' AND `book`.`author` LIKE \'%{author}%\' AND `book`.`genre` LIKE \'%{genre}%\';') 
            results = db.engine.execute(sql)
            if results.rowcount == 0:
                flash("Not Found", category='error')
            else:
                flash(f"Found {results.rowcount} results matching title {title}, genre {genre} and author {author}", category='success')
            return render_template("home.html", results = results)
        else:
            flash("An error occured", category='error')
    else:
        flash("No filter were assigned", category='success')
        sql = text(f'Select `book`.`judul`, `book`.`author`, `book`.`isbn`, `book`.`genre`, `book`.`img_path` FROM `book`;')  
        results = db.engine.execute(sql)
        return render_template("home.html", results = results)
    return render_template("home.html")

@views.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        judul = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        isbn = request.form.get('isbn')

        # check if the post request has the file part
        if 'cover' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['cover']

        NgecekadaJudulApaNggak = Book.query.filter_by(judul=judul, author=author).first()
        if NgecekadaJudulApaNggak:
            flash('Book already exist', category='error')
            return redirect(request.url)

        # #upload ke s3 dulu
        try:
            new_book = Book(judul = judul, author = author, isbn = isbn, genre = genre)
            db.session.add(new_book)
            db.session.commit()

            uploaded_book = Book.query.filter_by(judul=judul, author=author).first()
            uploaded_book_id = uploaded_book.id_buku

            # format nama file
            image_file_name_in_s3 = "cover_" + str(uploaded_book_id) + ".png"

            s3 = boto3.client('s3', region_name="us-east-1",
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key= keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN
                    )

            try:
                print("Data inserted in MySQL RDS... uploading image to S3...")   
                file.save(f"img/{image_file_name_in_s3}")
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename = f"img/{image_file_name_in_s3}",
                    Key = f"img/{image_file_name_in_s3}",
                    ExtraArgs={
                        "ContentType": 'image/png'
                    }
                )

                # update img_path di database
                updated_book = Book.query.get(uploaded_book_id)
                if not updated_book:
                    flash('Something went wrong.', category='error')
                    return redirect(request.url)
                updated_book.img_path = f"https://cc22book.s3.amazonaws.com/img/cover_{uploaded_book_id}.png"
                db.session.commit()
                
                flash("Book uploaded successfully", category="succeess")

            except Exception as e:
                return str(e)

        except Exception as e:
                return str(e)
                # return redirect("/")
    return render_template("upload.html")

@views.route('/upload-file', methods=['POST'])
def upload_file():
    
    # get the uploaded file
    files = request.files['file']
    final_path = os.path.join(ROOT_FOLDER,files.filename)
    files.save(final_path)

    # get id_kota
    kota_id = files.filename.strip("id_kota_.csv")
    
    # parse csv
    parseCSV(final_path, kota_id)
    return redirect(url_for('views.home'))