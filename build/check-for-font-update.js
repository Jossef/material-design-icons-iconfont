const common = require('./common');
const path = require('path');

async function main() {
    let hashPreUpdate = await common.calculateDirHash(common.DIST_DIR_PATH);
    await common.updateAndBuild();
    let hashPostUpdate = await common.calculateDirHash(common.DIST_DIR_PATH);

    let requireUpdate = hashPreUpdate !== hashPostUpdate;
    if (!requireUpdate) {
        throw new Error("nothing to update")
    }
    console.log(`an update is required ${hashPreUpdate} != ${hashPostUpdate}`);
}


main()
    .then(() => process.exit(0))
    .catch((e) => {
        console.error(e);
        process.exit(1)
    });


