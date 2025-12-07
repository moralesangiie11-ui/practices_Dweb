from flask import Blueprint, request, jsonify, render_template

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/ssr', methods=['GET'])
def list_movies_ssr():
    from .models import Movie 
    # Corrección Final: Convertir el QuerySet a una lista explícita para Jinja2
    all_movies = list(Movie.objects()) 
    return render_template('movie_list.html', movies=all_movies) 

@movies_bp.route('/', methods=['GET'])
def get_all_movies():
    from .models import Movie 
    
    genre_filter = request.args.get("genre")
    year_filter = request.args.get("year")
    
    query = {}
    
    if genre_filter:
        query['genre'] = genre_filter
        
    if year_filter:
        try:
            query['year'] = int(year_filter)
        except ValueError:
            return jsonify({"message": "El parámetro 'year' debe ser un número entero."}), 400

    filtered_movies = Movie.objects(**query)
    
    return filtered_movies.to_json(), 200

@movies_bp.route('/', methods=['POST'])
def add_movie():
    from .models import Movie 
    
    new_movie_data = request.get_json()
    
    if not new_movie_data or 'title' not in new_movie_data or 'genre' not in new_movie_data:
        return jsonify({"message": "Datos de película incompletos (requiere title y genre)"}), 400
    
    try:
        new_movie = Movie(**new_movie_data)
        new_movie.save()
        return new_movie.to_json(), 201 

    except Exception as e:
        return jsonify({"message": f"Error al crear la película: {str(e)}"}), 500

@movies_bp.route('/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    from .models import Movie 
    
    try:
        movie = Movie.objects(id=movie_id).first()
        
        if movie:
            movie.delete()
            return jsonify({"message": f"Película con ID {movie_id} eliminada"}), 200
        else:
            return jsonify({"message": f"Película con ID {movie_id} no encontrada"}), 404
            
    except Exception:
        return jsonify({"message": "ID de película inválido"}), 400