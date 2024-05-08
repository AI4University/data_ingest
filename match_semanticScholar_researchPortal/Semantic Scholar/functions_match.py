import string
def clean_string(string):
    '''
    Function for cleaning the string removing special characters

    Parameteres:
    string -> String to be cleaned
    
    Returns:
    string -> Cleaned inputed string
    '''
    
    # Lower case
    string = string.lower()
    
    # Remove ','
    string = string.replace(",", "")
    
    # Define characters to remplace (accents)
    changes = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
        'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
        'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o', 'ü': 'u',
        'ã': 'a', 'õ': 'o', 'ñ': 'n', 'ç': 'c',
    }

    # Perform the change
    for accent, not_accent in changes.items():
        string = string.replace(accent, not_accent)
        
    return string

def normalize_title(title):
    """
    Normaliza un título.

    Parámetros:
    title (str): El título a normalizar.

    Retorna:
    str: El título normalizado.
    """
    # Convertir a minúsculas
    if title is None:
        return None
    else:   
        title = clean_string(title)
        
        # Quitar signos de puntuación
        title = title.translate(str.maketrans('', '', string.punctuation))
        return title

def check_name(name1, name2):
    '''
    Function to identify if two names written in different format are the same

    Parameters:
    name1 -> First Name
    name2 -> Second Name

    Returns:
    same_name -> Boolean variable defining if the two inputed names are the same
    '''
    
    # Clean the names
    name1 = clean_string(name1)
    name2 = clean_string(name2)

    # Split the name in each of the elements
    name1_list = name1.split(' ')
    name2_list = name2.split(' ')

    #  Check if two names are the same
    same_name = False
    for name in name1_list:
        if name in name2_list:
            same_name = True
            break

    return same_name
    
def match_name_SS_RP(match_publis_SS_RP, researchers_publications_RP, researchers_publications_SS, researchers_RP, researchers_SS):
    '''
    Function for carrying out the match between researchers given the match between publications they have writen.

    match_publis_SS_RP -> DataSet containing the relationship between ids of the publications
    researchers_publications_RP -> DataSet containing the relationship between publications and authors in the Research Portal
    researchers_publications_SS -> DataSet containing the relationship between publications and authors in Semantich Scholar
    researchers_RP -> DataSet containing the authors in the Research Portal
    researchers_SS -> DataSet containing the authors in Semantic Scholar
    '''
    nuevas_filas = []
    total_filas = match_publis_SS_RP.count()
    contador_filas = 0
    checked = []
    
    # Obtain a table containing the relationship of the IDs of the researchers in the Research Portal and Semantic Scholar
    for fila in tqdm(match_publis_SS_RP.collect(), total=total_filas, desc="Progreso"):
        # Obtain a pair of IDs of publications (the correspondant one in the Research Portal and in Semantic Scholar)
        id_rp = fila.asDict()['ID_RP']
        id_ss = fila.asDict()['ID_SS']
    
        # Obtain the researchers for each of the publications in the Research Portal and in Semantic Scholar.
        df_publis_reserchers_rp = researchers_publications_RP.filter(col("actID") == id_rp)
        df_publis_reserchers_ss = researchers_publications_SS.filter(col("paper_id") == id_ss)
    
        # For each of the names in the Research Portal, look for its pair in Semantic Scholar
        for researcher_rp in df_publis_reserchers_rp.collect():
            id_researcher_rp = researcher_rp.asDict()['invID']
            name_rp = researchers_RP.filter(col("invID") == id_researcher_rp).collect()[0]['Name']
            for researcher_ss in df_publis_reserchers_ss.collect():
                id_researcher_ss = researcher_ss.asDict()['author_id']
                try:
                    name_ss = researchers_SS.filter(col("id") == id_researcher_ss).collect()[0]['name']
                except:
                    print('Aqui error (name):')
                    print('id_researcher_ss:', id_researcher_ss)
                    print('id_researcher_rp:', id_researcher_rp)
    
                # Verify that the names haven't been al ready checken
                if name_rp not in checked and name_ss not in checked:
                    if check_name(name_rp, name_ss):
                        try:
                            no_publis_ss = researchers_SS.filter(col("id") == id_researcher_ss).collect()[0]['papercount']
                            no_publis_rp = researchers_RP.filter(col("invID") == id_researcher_rp).collect()[0]['no_publis']
                            alias = researchers_SS.filter(col("id") == id_researcher_ss).collect()[0]['aliases']
                            nuevas_filas.append([name_rp, id_researcher_rp, name_ss, id_researcher_ss, no_publis_rp, no_publis_ss, alias])
        
                        except:
                            print('Aqui error (no publis):')
                            print('id_researcher_ss:', id_researcher_ss)
                            print('id_researcher_rp:', id_researcher_rp)       
                            
                    #checked.append(name_rp)
                    #checked.append(name_ss)
                    
                    # Borrar
                    # contador_filas += 1
                    # if contador_filas % 10 == 0:
                        # print(nuevas_filas[-10:])
    
    # Convertir las filas a tabla
    filas = [Row(name_RP=row[0], id_RP=row[1], name_SS=row[2], id_SS=row[3], no_publis_RP=row[4], no_publis_SS=row[5], aliases=row[6]) for row in nuevas_filas]
    return filas

def get_plot_publications(df, plot_type, x_legend):
    '''
    Function for obtaining the plot comparing the number of publications in Research Portal and in Semantic Scholar

    df -> DataSet containing the number of publications of each aouthor in SS and the RP
    plot_typ > bar or line
    x_legend -> Position in the x axis of the legend
    '''
    
    researcher_ids = df['id_RP']
    publications_RP = df['no_publis_RP']
    publications_SS = df['no_publis_SS']
    total_RP = sum(publications_RP)
    total_SS = sum(publications_SS)
    
    # Crear la figura y los ejes
    plt.figure(figsize=(20, 6))

    if plot_type == 'line':
        plt.plot(researcher_ids, publications_RP, label='Research Portal', alpha=0.5, marker='o', markersize=5)
        plt.plot(researcher_ids, publications_SS, label='Semantic Scholar', alpha=0.5, marker='o', markersize=5)
        
        #plt.fill_between(researcher_ids, publications_RP, color='skyblue', alpha=0.3)
        #plt.fill_between(researcher_ids, publications_SS, color='lightcoral', alpha=0.3)

    if plot_type == 'bar':
        plt.bar(researcher_ids, publications_RP, label='Research Portal', alpha=0.5)
        plt.bar(researcher_ids, publications_SS, label='Semantic Scholar', alpha=0.5)

    # Etiquetas y título
    plt.xlabel('Researcher ID')
    plt.ylabel('Number of Publications')
    plt.title('Comparison of Number of Publications in Research Portal and Semantic Scholar')
    
    # Añadir las etiquetas del eje x y rotarlas 90 grados
    plt.xticks(range(len(researcher_ids)), researcher_ids, rotation=90, fontsize=8)  # Rotar las etiquetas para mejor legibilidad
    plt.xticks(range(0, len(researcher_ids), 10))  # Mostrar solo cada segunda marca

    plt.text(x_legend, 0.75, f'Total Publications in RP: {total_RP}\nTotal Publications in SS: {total_SS}', transform=plt.gca().transAxes, 
             fontsize=10, ha='center', bbox=dict(facecolor='white', alpha=0.5))
    
    # Agregar una leyenda
    plt.legend()
    
    # Mostrar el gráfico
    #plt.grid(True) # Añadir rejilla
    plt.tight_layout()
    plt.show()