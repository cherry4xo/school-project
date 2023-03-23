import { action, computed, makeObservable, observable, toJS } from "mobx"

class AlbumPageParamsClass {

    params = null
    image = null
    trigger = false

    constructor() {
        makeObservable(this, {
            params: observable,
            changeParams: action,
            getParams: computed,
            getImage: computed,
            changeImage: action,
            image: observable,
            setLibraryTouchTrigger: action,
            getTrigger: computed,
            trigger: observable
        })
    }

    changeParams(newParams) {
        this.params = newParams
    }

    libraryTouchTrigger = false

    setLibraryTouchTrigger() {
        this.trigger = !this.trigger
    }

    get getTrigger() {
        return this.trigger
    }

    changeImage(newImage) {
        this.image = newImage
    }

    get getParams() {
        return this.params
    }

    get getImage() {
        return this.image
    }
}

export const AlbumPageParams = new AlbumPageParamsClass()