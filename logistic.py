import pgeocode
import math
import random

buyerpin = int(input("ENTER PINCODE"))
dist = pgeocode.GeoDistance('in')
h = dist.query_postal_code(buyerpin, buyerpin)

sellerpin = ["504293", "504231", "504201", "504312", "504295", "504106", "504306", "504299", "504202", "504103", "504306", "504293", "504346", "504296", "504302", "504311", "504309", "504273", "504313", "504304", "504299", "504272", "504296", "504209", "504297", "504307", "504299", "504207", "504251", "504219", "504105", "504273", "504219", "504297", "504293", "504311", "504001", "504101", "504205", "504102", "504214", "504304", "504219", "504206", "504204", "504103", "504106", "504204", "504206", "504313", "504311", "504306", "504299", "504204", "504323", "504310", "504105", "504203", "504216", "504306", "504307", "504309", "504105", "504303", "504109", "504203", "504294", "504209", "504110", "504206", "504102", "504251", "504110", "504201", "504001", "504299", "504203", "504299", "504296", "504103", "504308", "504204", "504001", "504273", "504307", "504272", "504272", "504201", "504299", "504202", "504218", "504205", "504206", "504296", "504309", "504311", "504251", "504273", "504309", "504102", "504312", "504312", "504295", "504309", "504215", "504299", "504103", "504313", "504296", "504220", "504313", "504203", "504299", "504310", "504293", "504308", "504104", "504103", "504299", "504297", "504299", "504208", "504207", "504206", "504296", "504313", "504103", "504104", "504215", "504203", "504251", "504105", "504306", "504299", "504313", "504299", "504312", "504310", "504106", "504293", "504105", "504201", "504293", "504203", "504251", "504001", "504273", "504304", "504001", "504313", "504346", "504306", "504299", "504292", "504312", "504346", "504323", "504308", "504309", "504308", "504299", "504296", "504216", "504346", "504296", "504110", "504312", "504205", "504109", "504101", "504304", "504207", "504203", "504307", "504201", "504105", "504312", "504311", "504299", "504105", "504202", "504310", "504231", "504297", "504304", "504216", "504297", "504299", "504102", "504307", "504205", "504202", "504219", "504203", "504311", "504201", "504346", "504304", "504304", "504309", "504205", "504001", "504313", "504312", "504001", "504309", "504110", "504103", "504307", "504307", "504103", "504307", "504214", "504323", "504204", "504304", "504309", "504103", "504110", "504101", "504103", "504103", "504304", "504103", "504201", "504110", "504231", "504103", "504001", "504346", "504219", "504109", "504273", "504205", "504310", "504001", "504106", "504346", "504204", "504216", "504308", "504292", "504323", "504273", "504304", "504202", "504312", "504104", "504214", "504307", "504251", "504299", "504209", "504214", "504292", "504292", "504106", "504214", "504219", "504313", "504109", "504251", "504001", "504205", "504207", "504219", "504311", "504308", "504206", "504323", "504307", "504297", "504106", "504346", "504216", "504101", "504273", "504001", "504251", "504202", "504299", "504205", "504251", "504323", "504299", "504310", "504306", "504001", "504102", "504304", "504293", "504311", "504311", "504292", "504208", "504306", "504299", "504295", "504216", "504251", "504231", "504313", "504219", "504293", "504273", "504309", "504312", "504301", "504214", "504106", "504215", "504208", "504209", "504297", "504001", "504207", "504292", "504105", "504104", "504313", "504103", "504202", "504201", "504310", "504001", "504216", "504106", "504273", "504272", "504346", "504216", "504313", "504251", "504304", "504311", "504272", "504001", "504209", "504313", "504309", "504101", "504311", "504304", "504101", "504101", "504251", "504296", "504110", "504206", "504202", "504294", "504346", "504102", "504104", "504304", "504307", "504110", "504309", "504299", "504106", "504215", "504313", "504207", "504292", "504103", "504311", "504309", "504207", "504109", "504208", "504231", "504104", "504219", "504215", "504214", "504346", "504302", "504309", "504296", "504299", "504105", "504307", "504299", "504296", "504346", "504296", "504309", "504201", "504312", "504312", "504102", "504109", "504308", "504205", "504215", "504296", "504215", "504308", "504323", "504001", "504346", "504307", "504001", "504273", "504296", "504201", "504204", "504293", "504273", "504001", "504311", "504309", "504308", "504203", "504310", "504215", "504207", "504293", "504311", "504346", "504214", "504304", "504102", "504231", "504106", "504216", "504109", "504273", "504106", "504313", "504296", "504299", "504214", "504307", "504104", "504308", "504201", "504311", "504312", "504001", "504251", "504346", "504102", "504104", "504296", "504292", "504302", "504308", "504206", "504296", "504106", "504295", "504109", "504313", "504101", "504103", "504311", "504251", "504215", "504001", "504205", "504294", "504001", "504299", "504207", "504201", "504307", "504102", "504311", "504304", "504215", "504273", "504299", "504293", "504311", "504205", "504313", "504306", "504299", "504295", "504201", "504310", "504110", "504323", "504206", "504103", "504110", "504103", "504293", "504311", "504311", "504106", "504311", "504203", "504216", "504109", "504346", "504304", "504110", "504307", "504310", "504301", "504202", "504107", "504297", "504296", "504201", "504307", "504001", "504204", "504293", "504216", "504001", "504294", "504346", "504219", "504251", "506343", "506223", "506244", "506015", "506347", "391115", "391125", "391135", "391110", "391140", "391145", "391250", "391105", "391160", "391135", "391168", "391152", "391152", "391140", "391165", "391150", "391160", "391170", "391160", "391105", "391121", "391121", "391110", "390001", "391145", "391150", "391105", "391250", "391121", "390001", "391121", "391121", "390019", "390019", "391150", "391135", "391107", "391130", "390004", "391107", "391125", "391120", "391165", "391150", "391160", "391152", "391160", "391105", "391130", "391165", "391150", "390001", "390014", "390011", "391250", "391140", "391160", "391105", "391107", "390009", "391150", "391160", "391150", "391145", "391168", "391107", "391155", "391135", "391135", "390009", "391120", "391160", "391170", "391165", "391250", "391150", "390019", "391168", "391125", "390019", "391145", "391165", "391125", "390009", "391110", "391152", "391165", "390014", "391145", "391145", "391160", "391107", "391168", "391110", "391125", "391160", "391110", "391135", "391170", "391152", "391168", "391105", "391170", "391160", "391170", "390004", "391168", "390006", "391165", "391170", "391107", "391135", "391140", "391110", "391152", "391140", "391250", "391110", "391168", "391120", "391110", "391110", "390022", "390006", "391150", "390022", "391150", "391150", "391125", "391175", "391150", "391120", "391170", "390019", "391125", "390010", "391105", "391115", "391250", "391125", "391155", "391150", "391125", "391110", "391121", "391168", "391165", "391155", "390009", "391110", "391110", "391105", "391168", "391152", "391115", "391121", "391120", "391145", "391110", "391170", "391125", "391160", "391135", "391150", "391121", "391160", "391125", "391130", "391150", "391152", "391150", "391250", "390013", "391170", "391107", "391165", "391135", "391120", "391168", "391105", "391165", "391168", "391160", "391110", "391168", "391105", "391135", "390019", "391120", "391115", "391125", "391121", "391160", "390010", "391135", "391110", "390022", "391120", "390017", "391160", "391145", "391135", "391160", "390001", "391160", "391105", "391135", "391140", "391165", "391120", "391165", "391160", "391165", "391120", "391135", "391150", "391125", "391160", "391140", "391160", "391140", "390004", "390018", "390001", "391168", "391107", "391145", "390001", "391160", "391160", "391120", "391120", "391145", "390019", "391170", "390004", "391140", "391145", "391250", "391250", "391110", "391130", "391160", "391120", "391250", "391121", "391105", "391120", "391152", "390025", "391107", "391105", "391121", "391160", "391160", "391250", "391150", "391165", "391168", "391107", "391145", "390022", "391121", "391168", "391150", "391160", "391130", "391115", "391168", "391110", "391115", "391155", "391152", "391145", "391168", "391168", "391135", "391145", "391130", "391152", "391150", "390025", "391125", "391105", "391152", "391107", "391740", "391445", "391761", "391410", "391240", "391440", "391440", "391760", "391340", "391101", "391445", "391243", "391430", "391330", "391220", "391760", "391240", "391774", "391770", "391430", "391761", "391510", "390016", "391530", "391430", "391780", "391410", "391243", "391780", "391520", "391761", "391430", "391240", "391244", "391530", "391440", "391244", "391510", "391330", "391745", "390021", "390012", "391780", "391774", "391761", "391760", "391210", "391780", "391410", "391244", "391774", "391440", "391340", "391240", "391243", "391440", "391320", "391520", "391210", "391761", "391220", "391761", "391770", "391220", "391440", "391520", "391430", "391775", "391340", "391530", "391440", "391350", "391770", "391243", "391510", "391330", "390023", "391244", "391520", "392310", "391770", "391530", "390007", "391761", "391244", "391243", "391750", "391440", "391774", "391510", "391430", "391520", "391310", "391430", "391510", "391760", "391510", "391440", "391210", "391520", "391244", "391510", "391345", "391760", "391780", "391445", "391760", "391440", "391440", "391450", "391510", "391445", "391243", "390007", "391760", "391510", "391510", "391240", "391346", "391530", "391210", "390007", "391760", "391240", "391774", "391240", "391761", "391440", "391450", "391421", "391220", "391780", "391210", "391210", "391520", "391530", "391445", "391350", "391761", "391410", "391350", "391440", "391243", "391240", "390020", "391760", "391101", "391761", "391240", "391445", "390012", "391445", "391430", "391510", "391520", "390012", "391450", "391510", "391240", "391240", "391775", "391440", "391530", "391440", "391243", "391240", "391770", "391440", "390007", "391340", "391510", "391530", "391770", "391761", "391440", "391760", "391770", "391101", "391244", "391775", "391775", "391530", "391430", "391761", "391774", "391770", "391760", "391775", "391745", "391244", "391775", "391510", "391530", "391430", "391210", "391510", "391520", "390016", "391240", "391240", "391530", "391210", "391775", "391240", "391240", "391220", "391240", "391774", "391220", "391445", "391510", "391520", "391240", "391430", "391220", "391243", "391440", "391774", "391745", "391421", "391760", "391310", "391520", "391410", "390003", "391244", "391440", "391740", "391774", "391510", "391450", "391740", "391761", "391210", "391520", "391440", "391760", "391760", "391774", "391220", "391760", "392310", "391761", "391761", "391421", "391770", "391780", "391346", "391780", "390002", "391445", "391243", "391740", "391240", "391330", "391760", "391774", "391760", "391520", "391445", "391440", "391510", "391510", "391445", "391330", "391330", "391510", "391445", "391421", "390024", "391740", "391210", "391760", "391450", "391244", "391440", "390008", "390002", "391760", "391430", "391510", "391761", "390003", "391770", "391240", "391774", "391243", "391510", "391210", "391761", "764070", "764002", "764056", "764052", "764077", "764072", "764044", "764063", "765024", "764058", "765026", "764061", "764039", "765029", "764074", "764047", "764037", "764074", "765025", "764074", "764005", "764001", "764049", "765019", "764014", "765019", "765029", "764043", "765026", "764085", "764074", "764043", "764020", "764045", "764087", "765020", "764021", "764087", "764058", "764074", "764061", "764043", "763004", "764044", "764078", "764027", "764056", "764038", "764036", "764045", "765023", "764002", "765016", "763002", "764078", "764077", "764027", "765001", "764027", "764086", "764039", "764056", "765025", "764045", "764042", "764059", "764027", "764049", "764037", "764073", "764073", "764076", "764043", "764014", "764002", "764073", "764057", "764056", "763008", "765020", "764072", "765019", "764044", "764043", "764036", "764077", "764043", "764071", "764011", "764039", "764002", "765015", "764072", "765019", "765018", "764075", "765024", "765034", "765002", "765033", "764045", "765019", "764036", "765016", "764055", "764002", "764036", "765016", "765013", "764051", "764027", "765025", "764037", "765017", "764056", "764047", "764072", "764020", "764056", "765015", "765002", "764055", "764044", "765013", "765024", "765026", "764061", "764078", "765015", "764045", "764077", "764028", "765023", "764047", "764071", "765023", "765019", "765023", "765017", "764003", "764039", "765019", "765002", "765013", "764056", "764051", "764039", "764038", "764036", "764043", "764056", "764005", "764036", "764002", "765002", "764039", "764063", "764072", "764073", "764037", "763001", "763002", "765016", "764039", "765018", "764081", "765015", "764088", "764038", "765025", "764055", "765026", "764075", "765020", "764072", "764073", "764052", "764041", "764072", "764075", "765019", "764061", "765029", "765024", "765026", "765015", "764028", "765022", "763003", "764003", "764028", "765020", "765019", "764051", "764058", "764043", "765026", "765029", "764037", "765017", "764071", "764074", "765019", "764049", "765017", "764021", "765002", "765033", "765026", "765026", "764075", "764055", "765023", "765022", "764074", "764074", "764071", "765015", "764043", "764044", "764047", "764021", "765013", "765015", "764074", "764044", "764052", "764077", "764071", "765017", "765013", "764047", "764044", "764052", "765022", "765026", "765015", "764036", "764071", "764074", "765015", "764003", "765022", "764043", "764070", "765022", "764074", "764047", "762018", "762026", "762015", "762103", "762010", "762104", "762014", "762014", "762002", "762109", "762104", "762104", "762101", "762103", "762011", "762018", "762019", "762012", "762012", "762020", "762021", "762027", "762016", "762010", "762029", "762102", "762011", "762021", "762015", "762014", "762018", "762024", "762014", "762103", "762105", "762103", "762011", "762013", "762030", "762017", "762021", "762015", "762015", "762101", "762104", "762101", "762016", "762018", "762029", "762102", "762101", "762012", "762109", "762020", "762014", "762112", "762109", "762012", "762026", "762013", "762012", "762016", "762103", "762107", "762105", "762017", "762011", "762015", "762024", "762104", "762011", "762103", "762107", "762101", "762028", "762011", "762018", "762001", "762002", "762014", "762001", "762010", "762100", "762026", "762103", "762011", "762105", "762110", "762022", "762104", "762014", "762002", "762026", "762026", "762002", "762029", "762022", "762030", "762016", "762028", "762106", "762014", "762103", "762028", "762002", "762102", "762024", "762030", "762029", "762021", "762023", "762107", "762021", "762101", "762015", "762015", "762100", "762011", "762016", "762030", "762026", "762109", "762105", "762101", "762030", "762112", "762101", "762109", "762029", "762015", "762100", "762103", "762028", "762112", "762002", "762011", "762101", "762103", "762107", "762017", "762021", "762023", "762021", "762012", "762013", "762104", "762010", "762110", "762024", "762029", "762014", "762103", "762002", "762016", "762027", "762100", "762104", "762011", "762002", "762106", "762014", "762022", "762020", "762024", "762012", "762020", "762001", "762110", "762011", "762017", "762105", "762112", "762110", "762100", "762024", "762023", "762100", "762011", "762002", "762020", "762011", "762030", "762106", "762002", "762021", "762010", "762015", "762103", "762021", "762002", "762103", "762101", "762100", "762100", "762022", "762012", "762012", "762112", "762101", "762028", "762101", "762105", "762029", "762106", "762023", "762103", "762012", "762014", "762104", "762012", "762014", "762002", "762106", "762101", "762107", "762105", "762014", "762102", "762106", "762101", "762104", "762011", "762028", "762024", "762104", "762104", "762100", "762104", "762002", "762104", "762013", "762112", "762015", "762020", "762017", "762030", "762101", "762110", "762103", "762011", "762106", "762107", "762101", "762024", "762109", "762015", "762010", "762014", "762020", "762101", "762103", "762104", "762018", "762107", "762101", "762014", "762102", "762013", "762020", "762104", "762020", "762021", "762110", "762027", "762021", "762020", "762107", "762011", "762106", "762029", "762001", "762027", "762015", "762015", "762110", "762026", "762106", "762110", "762020", "762012", "762110", "762104", "762010", "762015", "762017", "762107", "762011", "762107", "762011", "762015", "762030", "762102", "762105", "762100", "762002", "762015", "762100", "762024", "762023", "762021", "762021", "762002", "762021", "762110", "762002", "762102", "762100", "762105", "762106", "762103", "431143", "413249", "431143", "431515", "414204", "414208", "431128", "431123", "431153", "431127", "431130", "431128", "413249", "431517", "431153", "431131", "431127", "431130", "414208", "431124", "431144", "413207", "431515", "431123", "414205", "414203", "431124", "413249", "431126", "431123", "431153", "431515", "413207", "431131", "431153", "431131", "414205", "414208", "413229", "414205", "431520", "431523", "431530", "413229", "431127", "413249", "431127", "414202", "414202", "414203", "431517", "431143", "431153", "431144", "431153", "431523", "431129", "431127", "431123", "414203", "431153", "431127", "431143", "431123", "431125", "414203", "414203", "431153", "431517", "431515", "414203", "431519", "431142", "431129", "431131", "414203", "413207", "431131", "431123", "431530", "431123", "414202", "431129", "414202", "431126", "414203", "431125", "431123", "431127", "431130", "414202", "414204", "431515", "431517", "431517", "431144", "431130", "431128", "431143", "413229", "414208", "414208", "414205", "431153", "431123", "431515", "431131", "431123", "431515", "414204", "431127", "431131", "431523", "414205", "431123", "431153", "414202", "414203", "431131", "414204", "431144", "431129", "413249", "431125", "431123", "413207", "414202", "414205", "414203", "431153", "414202", "431127", "414204", "431128", "431126", "431518", "413229", "414203", "431130", "431153", "431142", "413207", "431517", "414202", "413249", "431128", "431519", "431126", "431143", "413229", "431153", "431129", "431517", "431517", "431143", "431129", "431123", "431123", "431144", "425301", "425201", "425201", "425107", "425306", "425307", "425305", "425108", "425309", "424208", "425301", "425311", "425107", "425306", "424206", "424204", "425107", "425107", "425107", "425306", "424206", "425309", "425508", "425503", "424205", "425508", "424207", "425501", "424208", "425308", "425305", "425107", "425108", "425524", "425310", "425327", "425302", "425507", "425108", "425503", "425306", "425503", "424206", "425508", "425310", "425107", "424204", "424207", "425108", "425503", "425306", "424206", "425107", "425508", "425310", "425201", "425504", "424206", "425114", "425107", "425504", "425301", "425502", "425502", "425306", "425108", "425503", "425304", "425303", "425107", "425302", "424208", "424204", "425310", "425508", "425311", "425107", "425504", "425310", "425301", "425311", "424206", "425306", "425504", "425114", "424205", "425327", "425327", "425306", "425508", "424206", "425304", "425107", "425310", "425502", "424207", "425311", "425507", "424207", "425507", "425508", "425310", "425306", "425311", "424208", "425114", "425503", "425307", "425114", "424206", "425108", "424206", "425303", "425508", "425507", "425302", "425301", "425114", "425302", "425504", "425303", "425508", "425301", "425311", "425508", "425301", "425302", "425507", "425304", "425302", "425303", "425311", "425308", "425504", "425502", "425327", "425524", "425302", "424204", "425310", "425306", "425306", "425302", "424204", "425311", "425107", "425305", "425311", "425108", "425508", "425305", "425107", "425304", "425505", "424208", "425107", "425310", "424208", "425310", "424206", "425303", "424206", "424207", "425508", "425310", "425304", "425114", "424206", "425309", "425308", "425108", "425301", "425305", "425107", "425107", "425302", "425303", "425508", "425201", "425506", "425303", "424206", "425107", "424206", "425107", "425310", "425306", "425107", "425310", "425505", "425504", "425502", "425524", "425107", "425327", "424206", "425203", "424206", "425501", "425303", "425107", "425107", "425503", "424206", "424205", "425107", "425108", "425304", "425203", "425201", "425301", "424204", "425302", "425301", "425203", "425501", "425310", "425306", "425107", "424204", "425203", "425307", "425114", "425307", "424206", "425310", "425114", "425506", "425306", "425503", "425305", "425504", "425307", "425310", "425107", "425502", "425305", "425306", "425327", "425107", "425508", "425508", "425405", "424305", "425410", "425417", "425412", "425421", "425411", "425405", "425403", "424304", "425406", "424308", "425414", "425408", "424308", "424005", "425409", "425407", "424301", "425418", "425424", "424311", "425419", "424304", "425409", "424310", "425452", "425424", "424304", "425416", "425416", "425418", "425416", "425408", "425412", "425432", "425405", "425432", "425411", "424308", "424318", "425442", "425409", "425416", "425418", "424302", "424304", "425408", "425412", "425408", "424307", "425432", "424305", "425407", "425409", "425409", "425444", "425406", "424303", "424304", "425417", "425416", "425414", "425413", "424306", "425442", "425406", "424311", "425408", "425406", "424305", "424318", "425413", "425412", "424006", "424304", "424002", "425426", "425412", "425410", "425428", "425444", "424306", "424304", "424006", "425408", "425416", "424001", "424001", "424304", "425405", "425410", "425432", "425405", "424302", "425414", "424306", "425405", "425442", "424303", "425408", "424304", "425452", "425409", "425403", "424301", "424308", "425412", "424306", "425404", "424304", "424306", "424310", "424006", "425414", "425415", "425413", "425407", "425416", "425407", "425412", "425407", "425426", "425413", "425421", "424004", "424306", "425423", "425405", "425442", "424307", "425411", "424310", "425405", "424306", "424306", "425418", "424304", "424310", "425416", "425424", "425432", "424301", "425407", "425411", "425412", "425408", "424307", "424310", "425405", "425414", "424305", "425409", "424311", "424302", "425413", "424303", "424002", "425403", "425405", "425418", "425408", "425411", "424006", "425407", "425412", "425405", "425405", "425409", "425413", "425414", "424311", "425442", "425408", "424305", "425422", "425412", "425405", "425428", "425403", "425409", "425413", "425415", "425417", "425409", "425427", "425452", "425414", "425412", "424311", "425432", "424301", "425414", "425407", "425426", "424001", "424006", "425412", "425408", "425423", "425412", "424308", "425406", "425409", "425408", "424303", "425408", "425417", "425432", "425413", "425414", "424002", "425412", "425412", "424002", "424306", "425452", "425424", "424304", "424308", "424309", "425405", "424304", "425427", "424302", "425405", "425452", "425408", "424002", "424304", "425409", "424301", "425406", "425404", "424304", "424305", "425412", "425428", "425444", "424304", "425408", "425452", "424305", "425409", "424002", "425426", "425452", "424304", "424002", "425412", "424001", "424002", "424304", "424309", "425426", "425406", "425408", "425444", "424306", "425412", "425442", "425409", "425423", "425404", "425418", "425444", "425414", "425405", "425405", "425412", "424305", "424305", "425428", "425412", "424302", "425409", "425406", "425428", "425442", "425416", "425419", "424310", "424005", "424307", "425422", "424318", "425418", "424305", "425416", "425409", "425412", "425409", "425414", "424002", "425405", "424304", "424306", "425416", "424306", "425406", "425409", "425408", "425419", "425421", "425412", "425423", "424318", "425404", "425405", "425412", "424311", "425405", "425427", "424310", "425416", "424305", "424305", "424304", "425444", "425422", "424307", "424302", "424304", "425412", "424002", "425408", "424310", "425405", "425405", "425415", "425405", "425432", "425412", "425416", "425422", "425426", "424304", "425423", "424002", "424006", "424307", "425444", "424002", "424308", "425412", "425412", "425404", "424311", "425412", "425405", "425413", "425419", "425432", "425406", "424304", "424304", "425410", "425408", "425409", "425412", "424318", "424306", "425412", "424306", "424306", "424002", "425427", "425426", "425405", "424309", "424309", "425405", "425407", "425427", "425419", "425416", "425412", "425426", "424307", "425407", "425417", "425414", "425414", "425418", "425406", "424307", "425412", "424001", "424004", "425417", "424002", "425406", "425414", "425408", "425418", "425412", "425413", "424002", "424002", "425406", "424002", "424309", "424304", "424318", "424306", "424306", "424304", "425412", "425412", "425427", "425421", "425423", "425444", "425427", "424318", "424309", "425411", "425408", "425404", "424301", "425415", "424303", "425421", "424304", "424302", "425406", "425413", "425405", "424304", "424306", "424306", "424002", "425419", "425408", "425421", "425423", "425407", "424304", "424307", "425419", "425423", "425409", "425408", "425421", "424304", "424002", "425418", "425418", "424318", "425408", "424311", "425412", "425417", "425432", "425422", "425418", "425405", "425414", "425412", "425405", "425409", "425427", "425428", "424311", "425432", "425428", "425405", "424305", "424310", "424002", "424306", "425420", "425401", "424104", "424119", "424119", "424119", "425105", "425420", "425109", "425002", "425001", "425001", "425402", "424201", "425109", "425103", "424107", "424119", "425115", "424202", "425401", "425105", "425111", "425004", "425401", "425002", "425420", "425115", "425401", "424105", "425401", "424203", "425401", "424105", "425104", "425111", "424102", "425002", "424119", "424104", "425110", "424119", "424119", "425103", "425401", "425115", "425101", "425003", "425111", "424105", "425109", "425102", "425105", "425402", "424119", "425401", "425401", "425401", "424106", "425103", "425401", "424119", "425104", "424102", "425001", "425105", "425002", "425116", "425401", "424104", "425111", "424119", "425420", "425103", "424103", "425401", "424119", "424108", "425111", "424119", "425401", "424202", "425109", "425116", "424102", "425103", "424104", "424201", "424106", "425109", "425104", "425116", "424203", "425002", "425401", "425110", "424108", "424201", "424108", "425002", "424201", "425002", "424106", "425003", "425111", "424104", "425105", "425115", "424201", "424201", "424119", "425104", "425103", "425105", "425111", "424119", "424201", "425109", "425115", "425103", "425110", "424104", "425401", "424201", "424201", "425102", "425401", "425113", "425116", "425402", "425401", "424119", "425111", "425001", "425001", "425116", "425002", "425003", "425401", "424201", "425401", "424105", "425401", "424119", "424201", "425103", "425105", "425105", "424119", "425105", "425109", "424119", "425002", "424119", "425110", "425111", "425115", "424201", "425116", "425113", "424108", "424101", "424106", "425105", "424201", "424103", "425113", "424107", "425103", "425402", "424119", "424201", "425105", "425401", "424106", "425002", "425402", "424104", "425401", "425113", "424202", "424103", "425111", "425109", "425111", "424119", "425401", "425111", "424201", "425002", "425109", "424101", "425003", "425003", "425105", "425111", "425111", "424106", "425401", "425401", "425001", "425401", "425420", "425110", "424119", "424105", "424202", "424201", "424103", "424106", "425111", "424105", "424102", "425002", "424107", "425111", "424201", "425104", "424103", "425002", "425105", "424108", "424119", "424119", "424106", "425401", "425002", "424105", "425002", "425113", "424106", "425115", "424119", "425111", "424101", "425112", "425420", "425109", "424108", "424106", "424103", "424106", "425111", "424106", "425401", "424103", "425115", "425003", "425002", "425402", "425110", "425115", "424119", "425420", "425105", "425115", "425105", "424201", "424119", "425105", "424103", "424102", "424202", "424119", "424201", "424105", "425002", "424119", "424101", "425103", "425103", "425111", "425401", "424201", "425420", "425401", "425002", "425109", "425105", "424119", "424108", "425111", "425001", "425111", "425105", "425002", "424105", "425103", "425401", "425401", "425111", "425111", "424104", "424105", "424201", "423101", "423104", "423303", "423301", "423501", "423117", "423105", "423102", "423105", "422303", "423204", "423401", "423502", "423202", "423301", "423106", "423117", "423106", "423206", "423301", "423104", "423301", "423102", "422305", "423102", "423502", "423105", "423104", "423401", "422305", "422303", "423212", "423104", "423301", "423302", "423102", "423108", "422306", "422209", "423302", "422205", "422205", "422306", "423204", "422205", "423106", "422304", "423206", "423102", "423102", "423205", "423401", "423402", "422205", "422205", "423502", "423204", "423213", "422305", "423401", "423106", "422209", "423502", "423301", "422209", "423204", "423105", "423403", "423301", "423501", "423205", "423501", "423401", "423111", "422306", "423206", "423105", "423501", "422303", "423208", "423301", "423401", "423501", "423402", "423301", "423117", "423206", "422306", "423206", "423401", "423302", "422305", "423201"]
print(len(sellerpin))
cost = [2,3,20,4]
n = []
threshwt = 10
# if buyerpin in levela:
#     level = 1
# elif buyerpin in levelb:
#     level = 2
# elif buyerpin in levelc:
#     level = 3
# else:
#     level = 4    
if math.isnan(h):
    print("PLEASE ENTER VALID PINCODE")
else:
    if len(sellerpin) == 0:
        print("NO SELLER SHIPS TO THIS PINCODE")
    else:
        logtype = float(input("Weight"))
        if logtype <= threshwt:
            print("1.COURIER")
        else:
            print("2.TRANSPORT")
        pin = str(buyerpin)
        a = dist.query_postal_code([pin], sellerpin)
        d = range(0,len(sellerpin))
        #print(d)
        for x in range(0,len(sellerpin)):
            #n.append(int(a[x])*cost[x])
            n.append(int(a[x])*random.random()*10)
        #b = n.tolist()
        c= n.index(min(n))
        print(sellerpin[c])