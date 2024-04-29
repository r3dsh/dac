
def handle(spec):
    # Step 1. process passed spec
    print("         ", __name__, "ZOMMMMM", spec)

    # Step 2. store secret value? or leave it to controller?
    # Step 3. return secret value
    return {
        "foo": "secret_bar",
    }


# def validate(spec):
#     print("         ", __name__, "VVVVALIDATE", spec)
#
#     return True
