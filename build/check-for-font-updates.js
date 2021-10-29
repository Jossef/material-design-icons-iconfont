const common = require('./common');
const path = require('path');

async function main() {
    let fontJsonFilePath = path.join(common.DIST_DIR_PATH, 'fonts', 'MaterialIcons-Regular.json');
    let hashPreUpdate = await common.calculateFileHash(fontJsonFilePath);
    await common.updateAndBuild();
    let hashPostUpdate = await common.calculateFileHash(fontJsonFilePath);

    let requireUpdate = hashPreUpdate.hash !== hashPostUpdate.hash;
    if (!requireUpdate) {
        console.log(`No update is required ${hashPreUpdate.hash} != ${hashPostUpdate.hash} == ${hashPreUpdate.hash !== hashPostUpdate.hash}`);
        throw new Error("nothing to update")
    }
    console.log(`an update is required ${hashPreUpdate.hash} != ${hashPostUpdate.hash}`);
}


main()
    .then(() => process.exit(0))
    .catch((e) => {
        console.error(e);
        process.exit(1)
    });


