from pyrum import SubprocessConn, Rumor
import trio


async def run(args):
    async with SubprocessConn(cmd='rumor bare') as conn:
        async with trio.open_nursery() as nursery:
            rumor = Rumor(conn, nursery)
            await rumor.host.start()

            # TODO: check type of result
            enr = await rumor.enr.make()

            await rumor.dv5.run(args['enr'])

            # TODO: result validation
            result = await rumor.dv5.ping(target=args['enr'])

            # TODO: result validation
            result = await rumor.dv5.lookup(target=args['enr')

            await rumor.dv5.cancel()

            nursery.cancel_scope.cancel()

            return (0, None)
