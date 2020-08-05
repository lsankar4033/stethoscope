from .utils import with_rumor

@with_rumor
async def run(rumor, args):
    try:
        await rumor.host.start()

        # TODO: check type of result
        enr = await rumor.enr.make()
        await rumor.dv5.run(args['enr'])

        # TODO: result validation
        result = await rumor.dv5.ping(target=args['enr'])
        # TODO: result validation
        result = await rumor.dv5.lookup(target=args['enr')

        await rumor.dv5.cancel()

        return 0

    except:
        return 1
