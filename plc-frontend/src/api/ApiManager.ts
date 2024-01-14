import { IEffectOptionsDefinition, IStatus } from '../domainData/DomainData';

const HOST = `http://${window.location.hostname}:8080`

const handleErrors = (res: Response) => {
    if (!res.ok) {
        throw new Error(res.statusText)
    }
}

export const setEffect = async (effectData: any) => {
    console.log(effectData);

    const res = await fetch(`${HOST}/effect/${effectData.effect}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        mode: "cors",
        body: JSON.stringify(effectData)
    })
    handleErrors(res)
    return res.json()
}

export const getAvailable = async (): Promise<string[]> => {
    const res = await fetch(`${HOST}/effect/available`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        mode: "cors"
    })
    handleErrors(res)
    return await res.json()
}

export const getStatus = async (): Promise<IStatus> => {
    const res = await fetch(`${HOST}/effect/current`, {
        method: "GET",
        mode: "cors"
    })
    handleErrors(res)
    return await res.json()
}

export const getOptionDefinition = async (effect: string): Promise<IEffectOptionsDefinition> => {
    const res = await fetch(`${HOST}/effect/${effect}/options`, {
        method: "GET",
        mode: "cors"
    })
    handleErrors(res)
    const unsorted: Record<string, any> = await res.json()
    const order = ["brightness", "effect"]
    const otherKeys = Object.keys(unsorted).filter((key) => !order.includes(key))
    const finalOrder = order.concat(otherKeys)
    const sorted: Record<string, any> = {}
    finalOrder.forEach((key) => {
        if (unsorted.hasOwnProperty(key)) {
            sorted[key] = unsorted[key]
        }
    })
    return sorted
}

export const addEffect = async (file: File, effectName: string) => {
    // validation
    if (!file || !effectName) {
        return
    }

    const formData = new FormData()
    formData.append("file", file)
    formData.append("effect_name", effectName)

    const res = await fetch(`${HOST}/upload/add`, {
        method: "POST",
        body: formData
    })

    handleErrors(res)
    return await res.json()
}

export const deleteEffect = async (effectName: string) => {
    const res = await fetch(`${HOST}/upload/delete/${effectName}`, {
        method: "DELETE"
    })
    handleErrors(res)
    return await res.json()
}