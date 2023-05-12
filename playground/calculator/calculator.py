import beaker as bk 
import pyteal as pt

class Mystate:
    result = bk.GlobalStateValue( pt.TealType.uint64 )

app = bk.Application( "Calculator", state = Mystate() )

@app.external
def add( a: pt.abi.Uint16, b: pt.abi.Uint16, *, output: pt.abi.Uint16 ) -> pt.Expr:
    add_result = a.get() + b.get()
    return pt.Seq(
        app.state.result.set( add_result ),
        output.set( add_result )
    )

@app.external( read_only = True )
def read_result( *, output: pt.abi.Uint16 ) -> pt.Expr:
    return output.set( app.state.result )

if __name__ == "__main__":
    spec = app.build()
    spec.export( "artifacts" )