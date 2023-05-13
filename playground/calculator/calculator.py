import beaker as bk 
import pyteal as pt

# Viene definita una classe chiamata Mystate, che contiene un'unica variabile di stato chiamata result
# result è un oggetto di tipo bk.GlobalStateValue di tipo pt.TealType.uint64
# Questa variabile di stato conterrà il risultato dell'operazione di aggiunta
class Mystate:
    result = bk.GlobalStateValue( pt.TealType.uint64 )

# Crea un'istanza di un'applicazione Beaker chiamata "Calculator" con lo stato iniziale "Mystate()"
app = bk.Application( "Calculator", state = Mystate() )

# Definizione della funzione "add" come un'operazione di aggiunta
# Calcola la somma dei parametri "a" e "b"
# Aggiorna il valore di "app.state.result" con "add_result"
# Imposta "add_result" come valore dell'output
@app.external
def add( a: pt.abi.Uint16, b: pt.abi.Uint16, *, output: pt.abi.Uint16 ) -> pt.Expr:
    add_result = a.get() + b.get()
    return pt.Seq(
        app.state.result.set( add_result ),
        output.set( add_result )
    )

# Definizione della funzione "read_result" per leggere il risultato dell'operazione di aggiunta senza modificare lo stato dell'applicazione
@app.external( read_only = True )
def read_result( *, output: pt.abi.Uint16 ) -> pt.Expr:
    # Imposta il valore attuale di "app.state.result" come valore dell'output
    return output.set( app.state.result )

# Compila l'applicazione Beaker
# Esporta l'applicazione compilata nella cartella "artifacts"
if __name__ == "__main__":
    spec = app.build()
    spec.export( "artifacts" )