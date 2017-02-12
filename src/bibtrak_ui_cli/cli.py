def get_args(raw_args):
    import argparse as argp

    parser = argp.ArgumentParser()

    command_parser = parser.add_subparsers(title="command")

    init_parser = command_parser.add_parser("init")
    add_parser = command_parser.add_parser("add")
    link_parser = command_parser.add_parser("link")

    init_parser.set_defaults(func=init_handler)
    add_parser.set_defaults(func=add_handler)
    link_parser.set_defaults(func=link_handler)

    add_parser.add_argument("handler__id")
    add_parser.add_argument("--id")

    link_parser.add_argument("id")
    link_parser.add_argument("filename")

    return parser.parse_args(raw_args)


def init_handler(args):
    from bibtrak import db
    db.init()


def add_handler(args):
    from bibtrak import db
    from bibtrak import handler

    from straight.plugin import load

    handlers = load("bibtrak.handlers", subclasses=handler.Handler)
    print("@@@HANDLERS@@@")
    print(handlers)

    for h in handlers:
        print(vars(h))

    handler_name, handler_id = args.handler__id.split(":", maxsplit=1)
    db_id = args.id or handler_id

    for h in handlers:
        if h.__name__ == handler_name:
            handler = h
            break
    else:
        raise Exception

    data = handler().fetch(handler_id)

    database = db.get_db_file()
    for key, value in data.items():
        db.insert(database, db_id, key, str(value))



def link_handler(args):
    from bibtrak import db

    database = db.get_db_file()
    db.link(database, args.id, args.filename)


def main(raw_args=None):
    if raw_args is None:
        import sys
        raw_args = sys.argv[1:]

    args = get_args(raw_args)

    args.func(args)

    return 0
