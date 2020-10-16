from stack import Stack
from graph import Graph

def simulate_following_endpoint(username):
    user_response = {
        'userA': ['userB', 'userD', 'userE', 'userG'],
        'userB': ['userC', 'userJ', 'userI', 'userE'],
        'userC': ['userM', 'userN', 'userJ', 'userI', 'userE']
    }
    return user_response[username] if username in user_response else []

def reorder_following_to_request(request_stack, current_following, has_stacked):
    index = len(current_following) - 1
    while index >= 0:
        if not current_following[index] in has_stacked:
            request_stack.push(current_following[index])
            has_stacked[current_following[index]] = 'na'
        index -= 1

def compute_distance(from_user, to_user):
    '''
        Basandose en el que no se posee previamente todos los datos de la estructura de los following, sino que
        se genera bajo demanda realizando consulta a los endpoints disponibles, el enfoque de solución que decidí
        utilizar es manteniendo un stack de requerimientos del following del actual usuario.
        Considero que bajo este enfoque se mantiene de forma óptima el uso de memoria y computo necesario, al mantener
        exclusivamente los datos necesarios e ir realizando la obtención de los datos faltantes de following
        desde los endpoints externos.
        Asumiendo que el orden de consultar los following, iniciaría siempre con el primer usuario al que 
        se le tiene como following se tendrá la siguiente estructura en generar nuestro stack de requerimientos.
        A partir de ello podemos definir la estructura de grafo de la red social para poder obtener la distancia
        entre 2 nodos, para lo cuál implemento el algoritmo de BreadFirstSearch obteniendo el camino más corto
        entre ambos nodos.
    '''
    request_stack = Stack()
    social_graph = Graph()
    has_stacked = {}
    following_from_users = simulate_following_endpoint(from_user)
    social_graph.add_node(from_user, following_from_users)
    reorder_following_to_request(request_stack, following_from_users, has_stacked)
    distance = -1
    while not request_stack.is_empty():
        current_element = request_stack.pop()
        current_following = simulate_following_endpoint(current_element)
        social_graph.add_node(current_element, current_following)
        distance = social_graph.compute_distance(from_user, to_user)
        if distance > 0:
            break
        if current_following:
            reorder_following_to_request(request_stack, current_following, has_stacked)
    return distance


if __name__ == '__main__':
    # El elemento ha sido encontrado si la distancia es >= 1, en caso de ser -1 el elemento no fue encontrado
    distance = compute_distance('userA', 'userM')
    print('Distancia entre A y M --> ', distance)
    print('*****************************')
    print('Additional Tests')
    print('Distancia entre A y G --> ', compute_distance('userA', 'userG'))
    print('Distancia entre A y T --> ', compute_distance('userA', 'userT'))
    print('Distancia entre B y N --> ', compute_distance('userB', 'userN'))
    '''
        Considerando la restricción de definir e implementar el algoritmo la solución planteada cumple
        el objetivo, en caso de requirir atender requerimientos con una red más compleja,
        de más de 1M de following/followers.
        Una solución con mejora de optimización para garantizar escalibilidad, sería definir e implementar
        el mecanismo de stack de request mediante una variante de desarrollo haciendo uso de un servidor
        Redis, lo cuál permita incrementar con mayor eficiencia mantener los request en espera.
        Adicional a esto dependiendo del lenguaje de programación se puede elegir una implementación de Grafo,
        con mejor eficiencia, en el caso de python una librería a escoger sería NetworkX
    '''
