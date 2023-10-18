type TEffectOptionsOutput = {
    [key: string]: any;
}

export interface IEffectOptionsDefinition {
    [name: string]: IEffectPropertyDefinition
}

export interface IEffectPropertyDefinition{
    type:string,
    constraint?:IConstraint
}

type TIntervalConstraintDefBounds = {
    inclusive: boolean
    value: number
}

export interface IIntervalConstraint{
    lower_bound:TIntervalConstraintDefBounds,
    upper_bound:TIntervalConstraintDefBounds
}

export interface IConstraint{
    type:string 
}

export interface IStatus extends Record<string, any> {
    effect:string,
    brightness: number
}

/*-------------------------------------*/

export interface IEffectOptionsRawDefinition{
    [name:string]:string
}

type KeyValueMap = {
    [key: string]: new (...args: any[]) => any;
};

export const Python2TsTypeMap:KeyValueMap = {
    "str" : String,
    "int" : Number,
    "float": Number,
    "type" : String,
    "typing.List[str]": Array<string>
}

export const python2TsTypeMapper = (rawType:string) => {
    return Python2TsTypeMap[rawType]
} 
